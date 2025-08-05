from pathlib import Path
from rich.console import Console
from rich.live import Live
from rich.spinner import Spinner

class ConsoleWriter():
    global console
    console = Console()

    def _spacer(lines : int = 1) -> None:
        """Print specified number of free lines."""
        space = ""
        for i in range(lines):
            space += "\n"
        return print(space)

    def file_deleted(path : Path, long_path : bool = False):
        """Print file deleted alert."""
        path = ConsoleWriter._get_path_type(path, long_path)
        ConsoleWriter._spacer()
        console.print(f'File {path} was [bold red]deleted[/] from disk.')

    def file_counts(sorted_files : dict) -> None:
        """Print overview about file types and their counts."""
        ConsoleWriter._spacer()
        console.print('[green]COUNTS OF FILE TYPES:[/]')
        for type in sorted_files.keys():
            type_count =  len(sorted_files[type])
            print(f'{type.upper()}: {type_count}')

    def select_file_types_input() -> str:
        """Ask for selection of type types to sort out, return user answer."""
        ConsoleWriter._spacer()
        return input('JAKÝ TYP SOUBOR SE MÁ VYTŘÍDIT? (text, docx, doc, pptx, pdf, spreadsheet, image, html)\n')

    def get_hash_counting_info() -> dict:
        ConsoleWriter._spacer()
        return {
            'start' : lambda: console.print('[cyan]Counting file hashes...[/]'),
            'hashing' : lambda file_type: f'Hashing {file_type}',
            'end' : lambda: console.print('[yellow]All hashes counted![yellow]'),
        }

    def file_similarity_score(score : float, path1 : Path, path2 : Path, long_path : bool = False) -> None:
        """Print info about similarity between two files."""
        path1 = ConsoleWriter._get_path_type(path1, long_path)
        path2 = ConsoleWriter._get_path_type(path2, long_path)
        ConsoleWriter._spacer()
        console.print(f'There is similarity [blue]{round(score * 100, 2)} %[/] between {path1} and {path2} files.')

    def do_you_want_to_remove_file(path : Path, long_path : bool = False) -> bool:
        path = ConsoleWriter._get_path_type(path, long_path)
        ConsoleWriter._spacer()
        if input(f'Do you want to delete the file {path}? (Y/n)\n') != 'Y':
            console.print(f'File {path} was [yellow]saved[/].')
            return False
        return True

    def file_still_open() -> None:
        """if one of processed files is open, print alert and stop process for a while."""
        input('One of the files is still open. Close it and press enter for continue.')

    def _get_path_type(path : Path, long_path : bool) -> Path:
        """Return selected type of path print."""
        if long_path:
            return path
        return path.name

    def detect_same_name_files() -> str:
        """Deteciting files with idetical name is in prograss information."""
        return 'Detecting files with identical name...'

    def same_name_files_count(pair_count : int) -> None:
        """Detecting files with identical name is completed, 
        add info about files count."""
        print(f'{pair_count} pairs of files with same name was detected.')

    def duplicity_file_name_detected(path1 : Path, path2 : Path) -> None:
        """Inform about file name duplicity."""
        ConsoleWriter._spacer()
        print(f'Duplicate file name {path1.name} was detected in folders\n{path1.parent}\n{path2.parent}.')

    def ask_remove_duplicity_name_files() -> str:
        """Ask user if he want to remove or keep one of the duplicity name files."""
        return input("Do you want to remove second file ?\n(Y - remove, n - keep file, All - remove all duplicities)")
    
    def duplicity_names_removing_completed() -> None:
        """Inform that removing of duplicity name files is completed."""
        ConsoleWriter._spacer()
        print("Removing of idetic named files is completed.")

    def explore_files_progress(found_files_count : int, erase : bool = True) -> None:
        """Add progress info into console during disk exploration."""
        console.print(
                    f'[cyan]Searching...[/cyan] Found: {found_files_count} files',
                    end='\r' if erase else '\n',
                    soft_wrap=True,
                    highlight=False,
                )

    def init_live_spinner():
        """"Initialize live spinner."""
        return console.status("[bold green]Porovnávám soubory...[/]", spinner="dots")

    def update_live_spinner(live : Live, erase : bool = False):
        """Uopdate live spinner content."""
        if erase:
            return live.update('')
        return ConsoleWriter._live_spinnner_content(live)

    def _live_spinnner_content():
        """Return live spinner with content."""
        return Spinner("dots", text="Comparing files...")

    def print(content : str) -> None:
        """Print into console via rich."""
        console.print(content)