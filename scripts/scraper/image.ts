import axios from 'axios';
import * as dotenv from 'dotenv';
import { getLogger } from './logger';

dotenv.config();

const UNSPLASH_ACCESS_KEY = process.env.UNSPLASH_ACCESS_KEY;

if (!UNSPLASH_ACCESS_KEY) {
  throw new Error('UNSPLASH_ACCESS_KEY is not defined');
}

const category = [
  {
    name: 'Furniture',
    subCategory: [
      { name: 'Bookcases', need: 583 },
      { name: 'Chairs', need: 647 },
      { name: 'Furnishings', need: 719 },
      { name: 'Tables', need: 381 }
    ]
  },
  {
    name: 'Technology',
    subCategory: [
      { name: 'Accessories', need: 700 },
      { name: 'Copiers', need: 537 },
      { name: 'Machines', need: 514 },
      { name: 'Phones', need: 733 }
    ]
  },
  {
    name: 'Office Supplies',
    subCategory: [
      { name: 'Appliances', need: 587 },
      { name: 'Art', need: 708 },
      { name: 'Binders', need: 781 },
      { name: 'Envelopes', need: 613 },
      { name: 'Fasteners', need: 583 },
      { name: 'Labels', need: 602 },
      { name: 'Paper', need: 825 },
      { name: 'Storage', need: 684 },
      { name: 'Supplies', need: 574 }
    ]
  }
];

const log = getLogger();

const instance = axios.create({
  baseURL: 'https://api.unsplash.com',
  headers: { Authorization: `Client-ID ${UNSPLASH_ACCESS_KEY}` }
});

const searchPhotos = async (query: string, page: number) => {
  log.info(`Searching for ${query}...`);
  const { headers, data } = await instance.get('/search/photos', {
    params: { query, page, per_page: 30 }
  });

  log.info(`Total pages: ${headers['x-total']}`);
  log.info(`Rate Limit Remaining: ${headers['x-ratelimit-remaining']}`);

  log.info(data.results.length);
};

searchPhotos('Furniture Furnishings', 1);
