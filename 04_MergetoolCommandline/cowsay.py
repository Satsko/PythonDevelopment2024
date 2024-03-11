import cowsay
import cmd
import shlex

class cmd_cowsay(cmd.Cmd):
    prompt = ">> "


if __name__ == "__main__":
    cmd_cowsay().cmdloop()
