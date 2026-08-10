import fs from 'fs';
import path from 'path';

export default function GeeReadmePage() {
  // 1. Point to your markdown file in the content folder
  const filePath = path.join(process.cwd(), 'content', 'gee_readme.md');
  
  // 2. Read the file contents
  const fileContent = fs.readFileSync(filePath, 'utf8');

  // 3. Display the content on the page
  return (
    <main style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
      <h1>Google Earth Engine Instructions</h1>
      
      {/* Displays the raw markdown text. Update this to use your 
          render.mjs function if you want it formatted as HTML! */}
      <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit' }}>
        {fileContent}
      </pre>
    </main>
  );
}