const { google } = require('googleapis');
const { GoogleAuth } = require('google-auth-library');
const { Buffer } = require('buffer');
const fs = require('fs');
const path = require('path');

async function fetchUpstreamSheet() {
  const credentialsJSON = Buffer.from(process.env.GOOGLE_APPLICATION_CREDENTIALS_BASE64, 'base64').toString('utf8');
  const credentials = JSON.parse(credentialsJSON);

  const auth = new GoogleAuth({
    credentials: credentials,
    scopes: ['https://www.googleapis.com/auth/spreadsheets.readonly'],
  });

  const client = await auth.getClient();
  const sheets = google.sheets({ version: 'v4', auth: client });
  const spreadsheetId = process.env.MYSTEN_SPREEDSHEET_ID;
  const range = 'Sheet1!A:H';

  const response = await sheets.spreadsheets.values.get({
    spreadsheetId,
    range,
  });
  const spreadsheetData = response.data.values;
  return {

    coin: extractAddressByType(spreadsheetData, 'Coin'),
    object: extractAddressByType(spreadsheetData, 'NFT').concat(extractAddressByType(spreadsheetData, 'Object')),
    package: extractAddressByType(spreadsheetData, 'Package'),
  }
}

function extractAddressByType(data, type) {
  // Filter out table headers and empty rows
  const filteredData = data.filter(row => row.length !== 0 && row[0] !== 'Type');

  // Define a function to determine if the address meets the format criteria based on type
  const meetsFormatCriteria = (row) => {
    if (row[0] === 'NFT' || row[0] === 'Coin' || row[0] === 'Object') {
      return row[2].includes('::');
    } else if (row[0] === 'package') {
      return !row[2].includes('::');
    }
    return false;
  };

  // Extract addresses of the specified type
  const addresses = filteredData
    .filter(row => row[0] === type && meetsFormatCriteria(row))
    .map(row => row[2]); // Formatted Address is in the third column

  return addresses;
}

function updateFile(spreadsheetData) {
  const fs = require('fs');
  const path = require('path');


  const types = Object.keys(spreadsheetData);
  console.log(types)
  types.forEach(type => {
    const filePath = path.resolve(__dirname, `../src/${type.toLowerCase()}-list.json`);
    // Read the existing JSON file
    let data = {};
    try {
      data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
      console.log(`Read ${type}-list.json successfully.`);
    } catch (error) {
      console.error(`Error reading file for ${type}:`, error);
      return;
    }

    // Merge new addresses into blocklist, sort and deduplicate
    const updatedBlocklist = Array.from(new Set([...data.blocklist, ...spreadsheetData[type]]));
    updatedBlocklist.sort();

    // Update blocklist and write back to the file
    data.blocklist = updatedBlocklist;
    try {
      fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
      console.log(`${type}-list.json updated successfully.`);
    } catch (error) {
      console.error(`Error writing file for ${type}:`, error);
    }
  });
}


async function run() {
  const sheetData = await fetchUpstreamSheet()
  updateFile(sheetData)
  // console.log(sheetData)
}

run().catch(console.error);