import cv2
import mediapipe as mp
import asyncio
from playwright.async_api import async_playwright

# Initialize Face Mesh (Lightweight for your RTX 3050)
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5)

async def run_agent():
    async with async_playwright() as p:
        # Launch Reddit
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://reddit.com")

        cap = cv2.VideoCapture(0) # Open Webcam

        while True:
            ret, frame = cap.read()
            if not ret: break

            # 1. ANALYZE FACE
            results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            
            if results.multi_face_landmarks:
                # Basic engagement logic: If mouth stretches (smile) or eyes widen
                # You can add specific MediaPipe landmark indices here
                is_enjoying = True # Placeholder for your trigger logic

                if is_enjoying:
                    # 2. AUTO-JOIN SUBREDDIT (Background Action)
                    try:
                        # Find the subreddit name of the current post on screen
                        sub_link = await page.query_selector('a[data-click-id="subreddit"]')
                        if sub_link:
                            await sub_link.click(button="middle") # Open in background
                            # Add logic here to click 'Join' in the new tab
                    except:
                        pass

            # 3. AUTO-SCROLL LOGIC
            # This scrolls down every 15 seconds, or you can trigger it 
            # by looking at the bottom of your screen.
            await page.mouse.wheel(0, 800) 
            await asyncio.sleep(15) # Wait for video/gif to play

        await browser.close()

asyncio.run(run_agent())
