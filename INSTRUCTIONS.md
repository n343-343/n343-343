# How to Use the Noakhali AI System

This file provides instructions on how to use the application.

---

## Easy Mode (for Beginners)

### English Instructions

**How to get your program:**

1.  Go to the **Releases** page on GitHub.
2.  Find the newest release.
3.  Click on `main.exe` to download it.
4.  Double-click the downloaded file to run the program.

### বাংলা নির্দেশাবলী (Bengali Instructions)

**কিভাবে আপনার প্রোগ্রামটি পাবেন:**

১. GitHub-এ **Releases** পেইজে যান।
২. নতুন রিলিজটি খুঁজুন।
৩. ডাউনলোড করার জন্য `main.exe`-তে ক্লিক করুন।
৪. ডাউনলোড করা ফাইলটিতে ডাবল-ক্লিক করে প্রোগ্রামটি চালান।

---

## Advanced Mode (for Developers)

### 1. How to Run the Application on Your Computer

To run the application locally, you will need to have Python 3 installed.

**Step 1: Install the necessary programs**

First, you need to install all the programs the application needs to run. Open a terminal or command prompt and run this command:

```bash
pip install -r ruinnakbe/requirements.txt
```

**Step 2: Run the application**

Once the installation is complete, you can start the application with this command:

```bash
python3 ruinnakbe/main.py
```

The application will now be running at [http://127.0.0.1:8080](http://127.0.0.1:8080).

### 2. How to Use the Docker Container

If you have Docker installed, you can use it to run the application in a container.

**Step 1: Build the Docker image**

First, you need to build the Docker image. Run this command from the main project folder:

```bash
cd ruinnakbe && sudo docker build . --file Dockerfile
```

**Step 2: Run the Docker container**

Once the image is built, you can run it with this command:

```bash
sudo docker run -p 8080:8080 <image_id>
```

(Replace `<image_id>` with the actual ID of the image you just built).

The application will now be running at [http://127.0.0.1:8080](http://127.0.0.1:8080).

### 3. How to Create a New Release

I have created a special, automatic system that will build a Windows `.exe` file and create a new release for you.

**Step 1: Go to the "Actions" tab in your GitHub repository**

Click on the "Actions" tab at the top of your repository page.

**Step 2: Find the "Create GitHub Release" workflow**

On the left side of the page, you will see a list of workflows. Click on **"Create GitHub Release"**.

**Step 3: Run the workflow**

You will see a button that says **"Run workflow"**. Click on it.

**Step 4: Enter a version number**

A small window will appear asking you to enter a version number. Type in a version number for your new release (for example, `v1.0.0`).

**Step 5: Click "Run workflow"**

Click the green "Run workflow" button. The system will now automatically:

1.  Build your `.exe` file.
2.  Create a new release on the "Releases" page.
3.  Upload the `.exe` file and the source code so it is ready for download.

That's it! You have now created a new release.
