# gui-tad

## Project definition

This project represent graphical user interface for development of interactive fiction.   
It is implemented using Python, specifically using PyQt6 library for GUI development   
and textX meta-language for defining game model.

Project is consisted of three parts:
- textX meta-model
- model interpreter
- GUI editor

---

## textX meta-model

This meta-model represents a domain-specific language that has   
its own grammar and defines the world in the game.   
It is defined using [textX meta-language](http://textx.github.io/textX/stable/)

---

## Model interpreter

Model interpreter loads created model and manipulates with it.   
Executes player commands on the model and monitors the current state of the world.   
It uses textX Python module for model loading and has complex logic of model manipulation.

---

## GUI editor

With this editor user can easily create worlds with interactive graphic tools.    
It enables model saving, generating and editing.

---

## Usage

When model is generated using editor it can be runned with interpreter    
using this command:

    python game/game.py path_to_your_model.wld