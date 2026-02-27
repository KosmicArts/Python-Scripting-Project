import os   
# provides access to ops such as managing files and directories

import json
# a lightweight syntax for storing and exchanging data

import shutil
# provides operations on files/dirs such as copy, move, remove, etc

from subprocess import PIPE, run
# used to open/run other programs and commands from python

import sys
# used to gain access to command-line arguments

# =======================================================================

'''
Project Steps/Requirements:

- Find all game directories from /data
- Create a new /games directory 
- Copy and remove the "game" suffix of all games into the /games directory
- Create a .json file with the information about the games
- Compile all of the game code 
- Run all of the game code
'''

# =======================================================================

GAME_DIR_PATTERN = "game";
GAME_CODE_EXTENSION = ".go";
GAME_COMPILE_COMMAND = ["go", "build"];

# 1. Find all game directories from /data
def find_all_game_paths(source):
    """
    Docstring for find_all_game_dirs
    
    :param source: where we're looking

    look through all the files/dirs in the given source dir,
    and if their names include "game", then they'll be added to
    a list.
    """

    game_paths = [];

    for root, dirs, files in os.walk(source):
        for directory in dirs:
            if GAME_DIR_PATTERN in directory.lower():
                path = os.path.join(source, directory);
                game_paths.append(path);

        break
    return game_paths

# =======================================================================

# 2. Create a new /games directory
def create_dir(path, newdir):
    if os.path.exists(path) == False:
        os.mkdir(path);
        print(f"The '{newdir}' dir has been created!");
    else:
        print(f"{newdir} already exists, and therefore cannot be created.");

# =======================================================================

# 3. Remove the "game" suffix from all games in the /data directory
def get_name_from_paths(paths, char_to_strip):
    new_names = [];

    for path in paths:
        # split the paths in each game path into the head(dont need this) and tail
        head, dir_name = os.path.split(path);
        # cut out and replace the _game(char_to_strip) from each tail(the file or dir)
        new_dir_name = dir_name.replace(char_to_strip, "");
        # add these new stripped names to the list and then return it
        new_names.append(new_dir_name);
    return new_names

# =======================================================================

# 4. Copy and move all games into the new target directory
def copy_and_overwrite(source, target_dest):
    if os.path.exists(target_dest):
        shutil.rmtree(target_dest);
    shutil.copytree(source, target_dest)

# =======================================================================

# 5. Create a .json file with the information about the games
def make_json_metadata_file(path, game_dirs):
    data = {
        "gameName": game_dirs,
        "numberOfGames": len(game_dirs)
    }
    
    # 'with' safely opens a file and then closes it after
    # 'w' = write, and will overwrite too
    with open(path, "w") as file:
        json.dump(data, file);

# =======================================================================

# 6. Compile all of the game code
def compile_game_code(path):
    code_file_name = None
    
    # look through all the contents of the given path directory
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(GAME_CODE_EXTENSION):
                code_file_name = file
                break
        break
    
    # end this loop if no file with GAME_CODE_EXTENSION is found
    if code_file_name is None:
        return

    # run the command to compile the game code
    comp_command = GAME_COMPILE_COMMAND + [code_file_name];
    run_command(comp_command, path);

# =======================================================================

# 7. Run all of the game code
def run_command(command, path):
    # get the directory we're in
    cwd = os.getcwd();

    # change into the directory w/ the code we want to run
    os.chdir(path);

    """
    PIPE helps communicate between python and 
    the process thats actually running the command. theoretically

    'run' runs in the cmd
    """

    # run the command to compile the code
    result = run(command, stdout=PIPE, stdin=PIPE, universal_newlines=True)
    print(f"Compile Result: {result}");

    # go back to the previous directory that we started in
    os.chdir(cwd);

# =======================================================================

def main(source, target):
    """
    Docstring for main
    
    source: the location we're searching in
    target: the new dir we want to create in source
    """
    
    cwd = os.getcwd();  # gets the current working dir
    source_path = os.path.join(cwd, source);
    target_path = os.path.join(cwd, target);

    # checks if the source recieved from the cmd actually exists before creating a new dir inside it
    if os.path.exists(source_path) == False:
        print(f"The {source} directory doesn't exist! Please try again.");
    else:
        # finds all the games directories in /data
        game_paths = find_all_game_paths(source_path);

        # create a new dir to store all the games we just found
        create_dir(target_path, target);

    # get a list of all the "game" dirs/file names with the suffix removed
    new_game_dirs = get_name_from_paths(game_paths, "_game");

    # loop through paths of all the games in /data coupled with the new dir names
    for src, dest in zip(game_paths, new_game_dirs):
        """
        1. loops through a list of the paths of all the games in /data
        zipped together with the names of the games with the '_game' suffix removed.
        EX: [('Python-Scripting-Project-main/data/hello_world_game', 'hello_world')]

        2. then combine the target path (the dir we want to copy into)
        with the new name of each game with the suffix removed. this creates dest_path
        EX: Python-Scripting-Project-main/data/hello_world
        
        3. then, we copy the games from /data and put them into dest_path

        4. finish by compiling the game code and making metdata
        """
        dest_path = os.path.join(target_path, dest);
        copy_and_overwrite(src, dest_path);
        compile_game_code(dest_path);
    print("Copy complete.")

    # create metadata and save it into the target directory
    json_path = os.path.join(target_path, "metadata.json");
    make_json_metadata_file(json_path, new_game_dirs);


# =======================================================================

if __name__ == "__main__":
    """
    ^ checks if this file is being run directly, 
    or is being imported as a module.

    DONT run any code if its being imported
    """

    """
    sys.argv is the arguments we put into the cmd, 
    which is then converted into a string
    """
    args = sys.argv;

    if len(args) != 3:
        raise Exception("You must pass a source and target directory - only!")
    
    source, target = args[1:];

    main(source, target);

# =======================================================================


