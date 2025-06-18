import express from 'express';
import redis from 'redis';
import { promisify } from 'util';

const app = express();
const port = 1245;

const listProducts = [
  { itemId: 1, itemName: 'Suitcase 250', price: 50, initialAvailableQuantity: 4 },
  { itemId: 2, itemName: 'Suitcase 450', price: 100, initialAvailableQuantity: 10 },
  { itemId: 3, itemName: 'Suitcase 650', price: 350, initialAvailableQuantity: 2 },
  { itemId: 4, itemName: 'Suitcase 1050', price: 550, initialAvailableQuantity: 5 }
];

function getItemById (id) {
  return listProducts.find(item => item.itemId === id);
}

const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

function reserveStockById (itemId, stock) {
  return setAsync(`item.${itemId}`, stock);
}

async function getCurrentReservedStockById (itemId) {
  const stock = await getAsync(`item.${itemId}`);
  return parseInt(stock) || 0;
}

// Routes
app.get('/list_products', (req, res) => {
  res.json(listProducts);
});

app.get('/list_products/:itemId', async (req, res) => {
  const id = parseInt(req.params.itemId);
  const product = getItemById(id);
  if (!product) return res.json({ status: 'Product not found' });

  const currentQuantity = product.initialAvailableQuantity - await getCurrentReservedStockById(id);
  res.json({ ...product, currentQuantity });
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const id = parseInt(req.params.itemId);
  const product = getItemById(id);
  if (!product) return res.json({ status: 'Product not found' });

  const currentStock = product.initialAvailableQuantity - await getCurrentReservedStockById(id);
  if (currentStock < 1) return res.json({ status: 'Not enough stock available', itemId: id });

  await reserveStockById(id, await getCurrentReservedStockById(id) + 1);
  res.json({ status: 'Reservation confirmed', itemId: id });
});

app.listen(port, () => {
  console.log(`API available on localhost port ${port}`);
});
