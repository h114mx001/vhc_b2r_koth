### game connections
import sqlite3
import docker
import re
import configparser

### times ultilties 
import time
from datetime import datetime, timedelta

### loggings & frontend 
from rich import box
from rich.align import Align
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.text import Text
from rich.layout import Layout
from rich.logging import RichHandler
import logging
from io import StringIO

######### constants ##########################
DEFAULT_KING = "NOT_KING"
config = configparser.ConfigParser()
config.read("config.ini")
database_connection = sqlite3.connect("koth.sqlite")

# Configurations
# points for becoming the new king 
TO_THE_NEW_KING = int(config["game"]["to_the_king"].strip())
# points for the rebellion that kills the old king
STOLEN_PERCENTAGE= int(config["game"]["stolen_percentage"].strip())
# points for the current king
LONG_LIVE= int(config["game"]["long_live"].strip())
# Length of a round, in seconds
ROUND_LENGTH = int(config["game"]["round_length"].strip())

######### helper functions ###################
def parse_ps_aux(output):
    lines = output.split('\n')[1:]  # Skip the header line
    processes = []
    for line in lines:
        if line:  # Skip empty lines
            fields = re.split(r'\s+', line)
            user = fields[0]
            pid = fields[1]
            command = ' '.join(fields[10:])
            processes.append((user, pid, command))
    return processes

def get_current_king() -> str:
    with open("king.txt", "r") as f:
        name = f.read().strip()
    # filter all sensitive characters to prevent sqli 
    return re.sub(r"[^a-zA-Z0-9_]", "", name)
# reset king
with open("king.txt", "w") as f:    
    f.write(DEFAULT_KING)
#############################################

### init scripts 

# Format the logging
############################################

#### Debugging utilities #####################

#############################################

class KoTH:
    # monitor the whole King of The Hill challenge
    def __init__(self):
        ### Docker clients
        self.client = docker.from_env()
        ### Boot2Root container
        self.b2r_container = self.client.containers.get("boot2root")
        ### Default king string
        self.current_king = DEFAULT_KING
        ### database setup... coming soon :)
        self.cursor = database_connection.cursor()

        ### frontend
        self.console = Console()
        self.console.size = (210, 52)

        ### layouts
        self.layout = Layout()
        # self.layout.size = None
        # self.layout.ratio = 2
        self.layout.split_column(Layout(name="banner"), Layout(name="upper"), Layout(name="lower"))
        self.layout["banner"].size = 17
        self.layout["upper"].size = 20
        self.layout["lower"].size = 15
        self.console.clear()

    def kill_all_process(self):
        # kill the process based on the process name
        # only accept:
        # 1. 'patch_{service_name}' 
        # 2. original process from the challenge

        ### Step 1: Get the process list
        try:
            exec_log = self.b2r_container.exec_run("ps aux", user='root')
            processes = parse_ps_aux(exec_log.output.decode())
        except Exception as e:
            print(f"Error: {e}")
            return False
        
        rules = ["python3 /home/werkzeug/sources/main.py", r"patch_[a-zA-Z0-9_]+"]

        ### Step 2: Kill the process that is not from the challenge/patch of the users
        try:
            for user, pid, command in processes:
                for rule in rules:
                    # if not match, kill the process
                    if re.search(rule, command):
                        # print(f"User: {user}, PID: {pid}, Command: {command}")
                        break
                    else:
                        self.b2r_container.exec_run(f"kill -9 {pid}", user='root')
                        # print(f"Killed process with PID {pid}")
                        break
        except Exception as e:
            print(f"Error: {e}")
            return False
        return True

    def monitor(self):
        # main workflow that will re-update every 10 minutes
        # TODO: 
        # - [x] 0. Shutdown all the process that is not from the challenge
        
        self.kill_all_process()
        # - [x] 1. Update leaderboard
        headline = self.point_update()
        self.logging_dashboard(headline)
        # 3. Logging the whole dashboard to terminal, announcing the next time the dashboard will be updated
    
    def point_update(self) -> str:
        updated_king = get_current_king()

        if updated_king == self.current_king == DEFAULT_KING:
            headline = "[bold yellow blink]No one has become the king![/] :crown: [bold yellow blink]Come and take the throne!!!![/]"
            return headline
        try:
            if updated_king == self.current_king:
                headline = f"[bold yellow blink]Current[/] :crown:: [bold yellow blink]{self.current_king}! Long live the King![/]"
                current_king_entry = self.cursor.execute(f"SELECT * FROM koth WHERE player_name = '{self.current_king}'").fetchone()
                self.cursor.execute(f"UPDATE koth SET points = {current_king_entry[3] + LONG_LIVE} WHERE player_name = '{self.current_king}'")
                return headline
            if updated_king != self.current_king:
                # do some point adding here... += 500 + old_king's points * 25%
                # create a new entry for the new king, if not exist
                # print("checking new king entry")
                new_king_entry = self.cursor.execute(f"SELECT * FROM koth WHERE player_name = '{updated_king}'").fetchone()
                if new_king_entry is None:
                    # wipe default data 
                    if self.current_king == DEFAULT_KING:
                        self.cursor.execute(f"DELETE FROM koth")
                    self.cursor.execute(f"INSERT INTO koth (player_name, last_king, points, count_kings) VALUES ('{updated_king}', 'a', 0, 0)")
                    new_king_entry = self.cursor.execute(f"SELECT * FROM koth WHERE player_name = '{updated_king}'").fetchone()

                # if this is the first time the king is updated (aka, self.current_king = DEFAULT), only add the TO_THE_NEW_KING points
                if self.current_king == DEFAULT_KING:
                    # set points     
                    headline = f"[bold yellow blink]Welcome to the first regime![/] :crown: [bold yellow blink]{updated_king}![/]"
                    # query = f"UPDATE koth SET points = {new_king_entry[3] + TO_THE_NEW_KING} WHERE player_name = '{updated_king}'"
                    self.cursor.execute(f"UPDATE koth SET points = {new_king_entry[3] + TO_THE_NEW_KING} WHERE player_name = '{updated_king}'")   
                else:
                    headline = f"[bold red blink]A rebelion has come![/] :crown: [bold yellow blink]{updated_king}[/] [bold white blink]has taken the throne from[/] [bold strike red blink]{self.current_king}[/]!"
                    old_king_entry = self.cursor.execute(f"SELECT * FROM koth WHERE player_name = '{self.current_king}'").fetchone()
                    self.cursor.execute(f"UPDATE koth SET points = {int(old_king_entry[3] - (STOLEN_PERCENTAGE/100) * old_king_entry[3])} WHERE player_name = '{self.current_king}'")
                    self.cursor.execute(f"UPDATE koth SET points = {int(new_king_entry[3] + TO_THE_NEW_KING + (STOLEN_PERCENTAGE/100) * old_king_entry[3])} WHERE player_name = '{updated_king}'")
                
                # set last king time
                self.cursor.execute(f"UPDATE koth SET last_king = '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}' WHERE player_name = '{updated_king}'")
                # set king count
                self.cursor.execute(f"UPDATE koth SET count_kings = {new_king_entry[4] + 1} WHERE player_name = '{updated_king}'")
                # update the current king
                self.current_king = updated_king
                return headline
        except Exception as e:
            print(f"Error: {e}")
            return False

    def logging_dashboard(self, headline: str): 
        # logging the whole dashboard to the terminal
        # TODO: 
        # 1. some fancy banner :)``
        # 2. print the current king `🎉 CURRENT 👑 {current_king} 🎉`
        # 3. logging the whole dashboard (based on the schema that will be provided later)
        # 4. print the next time the dashboard will be updated
        self.console.clear_live()
        self.log_capture_string = StringIO()
        self.log_console = Console(file=self.log_capture_string, force_terminal=True, )
        self.handler = RichHandler(console=self.log_console, rich_tracebacks=True)
        self.logger = logging.getLogger("rich")
        self.logger.addHandler(self.handler)
        FORMAT = "%(message)s"
        logging.basicConfig(
            level=20, format=FORMAT, datefmt="[%X]", handlers=[RichHandler(rich_tracebacks=True, show_time=True)],
        )
        with Live(self.layout, console = self.console, screen=False, refresh_per_second=50):
            banner = open("banner.txt", "r").read()
            self.layout["banner"].update(Text.from_markup(banner, justify="center", style="bold"))

            ### ranking table
            self.table = Table(show_footer = False)
            self.table_centered = Align.center(self.table)
            
            self.table.title = "VHC :crown: King of the Hill 🏰 - CECS Day 2024"
            self.table.title_style = "bold magenta"
            self.table.caption = "[b]Built by[/] [b magenta not dim]VinUni Hacking Club[/] :man_technologist: [b]with[/] [b red]love[/] :heart:"
            self.table.show_lines = True
            self.table.width = 150
            self.table.box = box.DOUBLE_EDGE
            headers = [":trophy: Ranking", "0xHacker", ":hundred_points: Points", ":crown: Last king time", ":checkered_flag: Kings count"]
            for header in headers:
                self.table.add_column(header, justify="center")

            
            self.cursor.execute("SELECT * FROM koth ORDER BY points DESC LIMIT 5")
            for index, row in enumerate(self.cursor.fetchall()):
                self.table.add_row(
                    f"#{index + 1}",
                    row[1],
                    f"{row[3]}",
                    f"{row[2]}",
                    f"{row[4]}"
                )           

            # Update the layout with the new table
            self.layout["upper"].update(self.table_centered)
            
            self.table.border_style = "bright_blue"
            self.table.rows[0].style = "bold yellow"
            self.logger.info("[bold blue]Leaderboard updated![/]", extra={"markup": True})
            self.logger.info(headline, extra={"markup": True})
            # logger.info("Table updated!")
            self.logger.critical("💀 [bold red blink]All non-challenge processes are killed![/]", extra={"markup": True})
            # log next reset in 10 minutes
            self.logger.warning(f":timer_clock: [bold yellow] Next reset: {(datetime.now() + timedelta(seconds=ROUND_LENGTH)).strftime('%Y-%m-%d %H:%M:%S')} [/]", extra={"markup": True})
            str_log = self.log_capture_string.getvalue()
            self.layout["lower"].update(Text.from_markup(str_log))
        return True

if __name__ == "__main__":
    koth = KoTH()
    while True:
        koth.monitor()
        time.sleep(int(ROUND_LENGTH))