# 📦 Inventory Tracking System 🚀

## 🌟 Overview
Welcome to the **Inventory Tracking System**, your ultimate tool for efficiently managing stock, tracking inventory values, and ensuring seamless business operations. Whether you're a small business owner or a supply chain manager, this system helps keep your inventory organized and optimized. 🏬📊

## ✨ Features
✅ **Add, Update, & Remove Items** – Manage your inventory effortlessly.
✅ **Real-Time Inventory Tracking** – Monitor inventory value over time.
✅ **Transaction History** – Keep a detailed log of all inventory changes.
✅ **Low Stock** – Get notified about items running low.
✅ **Data Persistence** – Store and retrieve inventory data in JSON format.

## 🛠 Technologies Used
🔹 **Python** – Core programming language.
🔹 **Dataclasses** – For structured data representation.
🔹 **JSON** – Lightweight storage for seamless data management.
🔹 **Math Module** – To power smart calculations.
🔹 **Datetime** – For precise transaction tracking.

## ⚙️ Installation
### 📌 Prerequisites
Make sure you have Python installed. Get it from [Python.org](https://www.python.org/downloads/).

### 🚀 Setup Steps
1️⃣ Clone the repository:
   ```sh
   git clone https://github.com/yourusername/inventory-management.git
   ```
2️⃣ Navigate to the project directory:
   ```sh
   cd inventory-management
   ```
3️⃣ Install dependencies (if required):
   ```sh
   pip install -r requirements.txt
   ```
4️⃣ Run the application:
   ```sh
   python main.py
   ```

## 📖 How to Use
### 🏷 Adding an Item
```python
inventory.add_item(Item(1, "Laptop", 5, 1200.0, "Electronics"))
```

### ❌ Removing an Item
```python
inventory.remove_item(1)
```

### 🔄 Updating an Item
```python
inventory.update_item(1, new_quantity=10, new_price=1100.0)
```

### 📉 Checking Low Stock Items
```python
low_stock = inventory.get_low_stock_items(threshold=5)
```

### 💾 Saving & Loading Data
```python
inventory.save_to_file("inventory_data.json")
inventory.load_from_file("inventory_data.json")
```

## 📂 Project Structure
```
Inventory-Management/
│-- backend/
│   ├── inventory.py  # Inventory management logic
│-- frontend/
│   ├── app.py  # User interface or API integration
│-- inventory_data.json  # Saved inventory data
│-- README.md  # Project documentation
```

## 📜 License
🔖 This project is licensed under the **MIT License**.

## 👥 Contributors
💡 **Treesha Bacchuwar** - Lead Developer & Architect

## 📬 Contact
📧 Feel free to reach out via **treesha2004@gmail.com** or check out my work on [GitHub](https://github.com/TreeshaBacchuwar)). 🚀

