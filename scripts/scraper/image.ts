import axios from 'axios';
import * as dotenv from 'dotenv';
import fs from 'fs';
import path from 'path';
import { getLogger } from './logger';

dotenv.config();

const UNSPLASH_ACCESS_KEY = process.env.UNSPLASH_ACCESS_KEY;
const FOLDER_PATH = path.join(__dirname, '../../resource/images');

if (!UNSPLASH_ACCESS_KEY) {
  throw new Error('UNSPLASH_ACCESS_KEY is not defined');
}

const log = getLogger();

const wait = (seconds: number) => {
  return new Promise(resolve => {
    setTimeout(resolve, seconds * 1000);
  });
};

const instance = axios.create({
  baseURL: 'https://api.unsplash.com',
  headers: {
    Authorization: `Client-ID ${UNSPLASH_ACCESS_KEY}`
  }
});

const searchPhotos = async (query: string, page: number) => {
  log.info(`Searching images for ${query} in Page ${page}`);

  const { headers, data, config } = await instance.get('/search/photos', {
    params: { query, page, per_page: 30 }
  });
  log.info(
    `Requested URL ${config.baseURL}${config.url}?${Object.entries(
      config.params
    )
      .map(([key, value]) => `${key}=${value}`)
      .join('&')}`
  );
  log.info(`Found ${data.results.length} photos`);
  log.info(`Total pages: ${headers['x-total']}`);
  log.info(`Rate Limit Remaining: ${headers['x-ratelimit-remaining']}`);

  return { data: data.results, remaining: headers['x-ratelimit-remaining'] };
};

const task = async (
  search: string,
  startPage: number,
  need: number,
  category: string,
  subCategory: string
) => {
  const folderPath = path.join(FOLDER_PATH, category);
  log.info(`Check if folder ${folderPath} exists`);

  if (!fs.existsSync(folderPath)) {
    log.info(`Folder ${folderPath} does not exist, creating`);
    fs.mkdirSync(folderPath);
  }

  const filePath = path.join(folderPath, `${subCategory}.txt`);
  log.info(`Check if file ${filePath} exists`);

  if (fs.existsSync(filePath)) {
    log.info(`File ${filePath} exists`);
  } else {
    log.info(`File ${filePath} does not exist`);
    log.info(`Create file ${filePath}`);
    fs.writeFileSync(filePath, 'raw,full,regular,small,thumb,small_s3\n');
  }

  log.info(`Starting task for ${search}`);
  let downloaded = 0;

  while (downloaded < need) {
    const { data, remaining } = await searchPhotos(search, startPage);

    data.map((item: any) => {
      const { raw, full, regular, small, thumb, small_s3 } = item.urls;
      const line = `${raw || '#'},${full || '#'},${regular || '#'},${
        small || '#'
      },${thumb || '#'},${small_s3 || '#'}\n`;

      fs.appendFileSync(filePath, line);
    });

    downloaded += data.length;
    log.info(`Downloaded ${downloaded} images, need ${need}`);

    startPage += 1;

    if (Number(remaining) === 0) {
      log.info(`Rate limit reached, waiting for 60 minute`);
      log.info('-------------------------------------------------------');
      await wait(60 * 60);
    } else {
      log.info(`Waiting for 5 seconds`);
      log.info('-------------------------------------------------------');
      await wait(5);
    }
  }

  log.info(`Task for ${search} completed`);
};

const category = [
  {
    name: 'Furniture',
    subCategory: [
      { name: 'Furnishings', need: 719 },
      { name: 'Bookcases', need: 583 },
      { name: 'Chairs', need: 647 },
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

const main = async () => {
  //Furniture
  // await task('Furniture Furnishings', 1, 1000, 'Furniture', 'Furnishings'); // Done
  // await task('Furniture Bookcases', 1, 1000, 'Furniture', 'Bookcases'); // Done
  // await task('Furniture Chairs', 1, 1000, 'Furniture', 'Chairs'); // Done
  // await task('Furniture Tables', 1, 1000, 'Furniture', 'Tables'); // Done
  //Technology
  // await task('Technology Phones', 1, 1000, 'Technology', 'Phones'); // Done
  // await task('Technology Accessories', 1, 1000, 'Technology', 'Accessories'); // Done
  // await task('Technology Copiers', 1, 1000, 'Technology', 'Copiers');  // Done
  // await task('Technology Machines', 1, 1000, 'Technology', 'Machines');  // Done
  //Office Supplies
  // await task('Office Supplies Binders', 1, 1000, 'Office Supplies', 'Binders');  // Done
  // await task(
  //   'Office Supplies Appliances',
  //   1,
  //   1000,
  //   'Office Supplies',
  //   'Appliances'
  // ); // Done
  // await task('Office Supplies Art', 1, 1000, 'Office Supplies', 'Art');
  // await task(
  //   'Office Supplies Envelopes',
  //   1,
  //   1000,
  //   'Office Supplies',
  //   'Envelopes'
  // );
  // await task('Office Supplies Fasteners', 1, 1000, 'Office Supplies', 'Fasteners');
  // await task('Office Supplies Labels', 1, 1000, 'Office Supplies', 'Labels');
  // await task('Office Supplies Paper', 1, 1000, 'Office Supplies', 'Paper');
  // await task('Office Supplies Storage', 1, 1000, 'Office Supplies', 'Storage');
  // await task('Office Supplies Supplies', 1, 1000, 'Office Supplies', 'Supplies');
};

main();
