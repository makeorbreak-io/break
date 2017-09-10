<p align="center">
  <img src="https://github.com/portosummerofcode/break/blob/master/logo.png" width="300">
</p>

<h3 align="center" style="margin: 0 auto">All the tasks in one place<!-- Serve Confidently --></h3>
<p align="center" style="margin: 0 auto">Project developed during Make or Brake 2017</p>

---

## What is it?
**TODOS** is a tool designed to simplify the developers work. In short, it concentrates the all annotations sprinkled around your code in just one place. No more `TODOs` that are forgotten, `FIXMEs` that are never fixed, or `NOTEs` who noone will notice ever again. And because it is customizable, you can adapt it to your needs.

At this point, you may use **TODOS** to output your annotations either as a text file, Github issues or Trello cards. Since it is a command line tool, it is easily configurable to run on a key combination on most text editors. Instructions for Visual Studio Code are provided later in this document.

![](https://github.com/portosummerofcode/break/blob/4b7b51be8eaf21c79aede0f1a902e1e8c015fa91/example.png?raw=true)

## Installation

**TODOS** has only been tested on Ubuntu 17.04 so far. It should work on similar systems without too many problems, but we can provide absolutely no guarantees.

In order to install it, you must first download the `tar.gz` from [here](https://github.com/portosummerofcode/break/raw/master/dist/todos-0.1.tar.gz). Also make sure that you have `python` and `pip` installed on your system. Once the download is complete open the directory where you've stored the `tar.gz` and do:

```
$pip install todos-0.1.tar.gz
```

## Usage

The basic usage of the tool requires only two commands to be remembered. Those are `todos init` to create the `todosconfig.toml` file that contains the configuration variables and `todos` to generate the output. In order to start using it in your project then just do:

```
$cd root_to_your_project/
$todos init
```

After entering all the necessary fields, you'll notice that a `todosconfig.toml` file was created. **TODOS** will process the tags `TODO`, `FIXME` and `NOTE` by default but you can change this. Just open `todosconfig.toml` and you'll find something like:

``` toml

[tags]
TODO = "yellow"
FIXME = "red"
NOTE = "green"

```

Change the values under `[tags]` to whichever ones best suit your style. So that the tool can recognize your annotations you must write your comments with the syntax:

```
// TODO(joaosilva22): This is a comment
// FIXME: This is another comment
// ...
```

## Adding a Key Bind to Visual Studio Code

In order to cause the least disruption to your usual workflow, you may add a key binding to your text editor that runs **TODOS** without having to switch to a terminal.

In VSCode all you need to do is create a custom task. To do that, click on `Tasks > Configure Tasks > Others` and copy this to `tasks.json`.

``` json
{
    "version": "2.0.0",
    "tasks": [
        {
            "taskName": "todos",
            "type": "shell",
            "command": "todos"
        }
    ]
}
```

Then open `File > Preferences > Keyboard Shortcuts` and copy the next snippet to `keybindings.json`.

``` json
{
    "key": "alt+t",
    "command": "workbench.action.tasks.runTask",
    "args": "todos"
}
```

Now every time you press `alt + t` the tool will run.

## Authors

<table rules=none>
  <tr>
    <td>
      <img src="https://avatars1.githubusercontent.com/u/15276733?v=4&s=400" width="100">
    </td>
    <td>
      João Silva<br />
      <a href="mailto:kontakt@wojtekmaj.pl">j.pedro004@gmail.com</a><br />
    </td>
    <td>
      <img src="https://avatars0.githubusercontent.com/u/17434192?v=4&s=400" width="100">
    </td>
    <td>
      Margarida Viterbo<br />
      <a href="mailto:kontakt@wojtekmaj.pl">margaridaviterbo@hotmail.com</a><br />
    </td>
  </tr>
  <tr>
    <td>
      <img src="https://avatars3.githubusercontent.com/u/12536106?v=4&s=400" width="100">
    </td>
    <td>
      José Martins<br />
      <a href="mailto:kontakt@wojtekmaj.pl">lluismmartins7@gmail.com</a><br />
    </td>
    <td>
      <img src="https://avatars0.githubusercontent.com/u/17434192?v=4&s=400" width="100">
    </td>
    <td>
      Rui Carvalho<br />
      <a href="mailto:kontakt@wojtekmaj.pl">margaridaviterbo@hotmail.com</a><br />
    </td>
  </tr>
</table>


 
