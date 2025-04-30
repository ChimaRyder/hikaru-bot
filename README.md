# ♟ Hikaru Chess Bot

A simple chess-playing AI bot built with TensorFlow. The project includes a Jupyter Notebook for model training and a Flask API to play against the trained bot.

The original training was done on Hikaru Nakamura games. Due to a lack of resources, the model was trained with only 2000 games.

## 📁 Project Structure

. ├── hikaru.ipynb # Jupyter Notebook for training the model ├── api.py # Flask API to interact with the bot ├── model/ # Folder to store trained model files ├── requirements.txt # Dependencies └── README.md # You're here!


## 🚀 Features

- Train a chess-playing model using historical game data (e.g., from Hikaru Nakamura).
- Expose the bot via a simple REST API using Flask.
- Play moves and respond with the AI's move.

## 🧠 Training the Model

Open the Jupyter Notebook:

```bash
jupyter notebook chess_bot.ipynb
```

Make sure to have your dataset ready and follow the notebook steps to:

    Load and preprocess the data.

    Build a model with TensorFlow.

    Train and evaluate the model.

    Save the trained model to the model/ directory.

## 🌐 Running the Flask API

After training and saving the model:

```bash
python api.py
```

The server will start at http://127.0.0.1:8000.

### API Endpoint

#### POST /bestmove

Request JSON:

```
{
  "pgn": "{Game PGN as string}"
}
```
 
Response JSON:

```
{
  "move": "e2e4"
}
```

## 📦 Installation

Install dependencies:

```
pip install -r requirements.txt
```

Make sure you have Python 3.7 or above.


## 📁 Requirements

    Python 3.7+

    TensorFlow

    python-chess

    Flask
