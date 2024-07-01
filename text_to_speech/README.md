Synthesizer is a Flask application built in Python.

Prerrequisites:
- Python 3.12
- Rust. Install running `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y` and then source your shell configuration eg `source ~/.zshrc` or `source ~/.bashrc`

Run app with 

```
flask --app synthesizer_app run
```

```
curl -XPOST http://127.0.0.1:5000/synthesize -d '{ "text": "husein wangi tetapi ketiak masam nasib baik kacak" }' -H "Content-Type: application/json"
```