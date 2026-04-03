import { Application } from 'https://unpkg.com/@splinetool/runtime@1.12.51/build/runtime.js';

const canvas = document.getElementById('spline-canvas');
const spline = new Application(canvas);

spline
  .load('https://prod.spline.design/DnXAqtyKw-iDe3dt/scene.splinecode')
  .then(() => {
    console.log('Spline scene loaded');
    // Hide spline watermark
    hideSplineWatermark();
  })
  .catch((err) => {
    console.error('Spline failed to load', err);
  });

// Hide spline branding/watermark
function hideSplineWatermark() {
  const watermarkSelectors = [
    '[style*="bottom: 12px"][style*="right: 12px"]',
    '[class*="watermark"]',
    '[class*="branding"]'
  ];
  
  watermarkSelectors.forEach(selector => {
    document.querySelectorAll(selector).forEach(el => {
      if (el && el.textContent.includes('Spline')) {
        el.style.display = 'none !important';
        el.style.opacity = '0 !important';
        el.style.visibility = 'hidden !important';
      }
    });
  });
}

// Run after a delay to catch elements added after load
setTimeout(hideSplineWatermark, 500);
setTimeout(hideSplineWatermark, 1500);

// Keep canvas sized to the window
function resize() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}
window.addEventListener('resize', resize);
resize();
