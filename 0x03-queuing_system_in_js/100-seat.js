import express from "express";
import redis from "redis";
import kue from "kue";
import { promisify } from "util";

const app = express();
const port = 1245;

const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

// Kue queue
const queue = kue.createQueue();

let reservationEnabled = true;

function reserveSeat(number) {
  return setAsync("available_seats", number);
}

async function getCurrentAvailableSeats() {
  const seats = await getAsync("available_seats");
  return parseInt(seats, 10);
}

// Setting initial seat count to 50
reserveSeat(50);

app.get("/available_seats", async (req, res) => {
  const seats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: seats.toString() });
});

app.get("/reserve_seat", (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: "Reservation are blocked" });
  }

  const job = queue.create("reserve_seat").save((err) => {
    if (err) {
      return res.json({ status: "Reservation failed" });
    }
    res.json({ status: "Reservation in process" });
  });

  job.on("complete", () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on("failed", (err) => {
    console.log(`Seat reservation job ${job.id} failed: ${err.message}`);
  });
});

app.get("/process", async (req, res) => {
  res.json({ status: "Queue processing" });

  queue.process("reserve_seat", async (job, done) => {
    let currentSeats = await getCurrentAvailableSeats();

    if (currentSeats <= 0) {
      reservationEnabled = false;
      return done(new Error("Not enough seats available"));
    }

    currentSeats -= 1;
    await reserveSeat(currentSeats);

    if (currentSeats === 0) {
      reservationEnabled = false;
    }

    done();
  });
});

// Starting the server
app.listen(port, () => {
  console.log(`API available on localhost port ${port}`);
});
