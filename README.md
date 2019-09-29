# MineTheBill @OlivettiCashRegister4.0-Hackathon - Backend component

Are you the owner of a small shop? Would you like to increase customer satisfaction and in a cheap, smart and seamless way?

MineTheBill is an Android app 📱for Olivetti's Smart Cash Register that, at every purchase inside a shop, generates a series of recommended discounts 💰based on the purchase history to improve customer loyalty and engagement.

MineTheBill realized during Olivetti Cash Register 4.0 Hackaton @EIT Digital CLC in Espoo, Finland.

## Setup

Create the new setup by using a virtual enviroment client such as `python venv` or `virtualenv`.

For instance:

```bash
 $ python -m venv ./venv
```

Activate the environment and install requirements:

```bash
 $ source venv/source/activate
 (venv) $ pip install -r requirements.txt
```

## Run the app

So far there is enough to start the `Flask` server (not recommended for production):

```bash
(venv) $ flask db upgrade; gunicorn minethebill:app
```

The `flask` command relies on the `FLASK_APP` environment variable defined in `.flaskenv`.
