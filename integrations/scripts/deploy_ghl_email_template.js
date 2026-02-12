#!/usr/bin/env node

/**
 * Generic Email Deployment Script
 * Use this as a template to deploy any new email to HighLevel.
 * 
 * USAGE:
 * 1. Duplicate this file (e.g., deploy-new-offer.js)
 * 2. Update the "Email Details" section below
 * 3. Run: node deploy-new-offer.js
 */

const https = require('https');

// Configuration
const API_KEY = process.env.VITE_HIGHLEVEL_TOKEN || 'YOUR_API_KEY_HERE';
const LOCATION_ID = process.env.VITE_HIGHLEVEL_LOCATION_ID || 'YOUR_LOCATION_ID_HERE';

// ==========================================
// EMAIL DETAILS - UPDATE THIS SECTION
// ==========================================
const TEMPLATE_NAME = 'My New Email Template';
const SUBJECT_LINE = 'My Subject Line';
const FROM_NAME = 'Mauricio Valencia';
const FROM_EMAIL = 'mauricio@stokeleads.com';
const PREVIEW_TEXT = 'Preview text here...';

const HTML_CONTENT = `
<html>
  <head>
    <style>
      body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; padding: 20px; }
      p { margin: 15px 0; }
    </style>
  </head>
  <body>
    <p>Hi {{contact.first_name}},</p>
    <p>Your content here...</p>
    <p>Best,<br>Mauricio</p>
  </body>
</html>
`;
// ==========================================

function request(path, method, data = null) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'services.leadconnectorhq.com',
      path: path,
      method: method,
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Version': '2021-07-28',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    };

    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', (d) => body += d);
      res.on('end', () => {
        try {
          const parsed = body ? JSON.parse(body) : {};
          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve({ status: res.statusCode, data: parsed });
          } else {
            resolve({ error: true, status: res.statusCode, body: body, data: parsed });
          }
        } catch (e) {
          resolve({ error: true, message: e.message, body });
        }
      });
    });

    req.on('error', (e) => reject(e));
    if (data) req.write(JSON.stringify(data));
    req.end();
  });
}

async function deploy() {
  console.log(`🚀 Deploying "${TEMPLATE_NAME}"...`);

  if (API_KEY === 'YOUR_API_KEY_HERE') {
    console.error('❌ Error: Please set your API_KEY in the script or .env file');
    process.exit(1);
  }

  try {
    // 1. Check for existing
    const listRes = await request(
      `/emails/builder?locationId=${LOCATION_ID}&limit=100`,
      'GET'
    );
    
    const templates = listRes.data.builders || listRes.data.data || [];
    const existing = templates.find(t => t.name === TEMPLATE_NAME && !t.archived);
    
    let templateId;

    if (existing) {
      console.log(`✓ Found existing template (${existing.id}). Updating...`);
      templateId = existing.id;
    } else {
      console.log(`+ Creating new template shell...`);
      // 2. Create Shell (Step 1 of 2)
      const createRes = await request('/emails/builder', 'POST', {
        locationId: LOCATION_ID,
        name: TEMPLATE_NAME,
        type: 'html'
      });

      if (createRes.error) throw new Error(`Create failed: ${JSON.stringify(createRes)}`);
      templateId = createRes.data.id;
      console.log(`✓ Shell created (${templateId}).`);
    }

    // 3. Patch Content (Step 2 of 2 - Critical for content to stick)
    console.log(`📝 Pushing content via PATCH...`);
    const updateRes = await request(`/emails/builder/${templateId}`, 'PATCH', {
      locationId: LOCATION_ID,
      name: TEMPLATE_NAME,
      subjectLine: SUBJECT_LINE,
      fromName: FROM_NAME,
      fromEmail: FROM_EMAIL,
      previewText: PREVIEW_TEXT,
      editorContent: HTML_CONTENT,
      editorType: 'html',
      updatedBy: 'deploy-generic-script'
    });

    if (updateRes.error) throw new Error(`Update failed: ${JSON.stringify(updateRes)}`);
    console.log(`✅ Success! Email deployed.`);

  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
}

deploy();
