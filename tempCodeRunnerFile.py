import random
import smtplib
import json
import time

import project

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich import box

console = Console(force_terminal=True, color_system="truecolor")


# =========================================================================
# LOGIN
# =========================================================================
def login():
    with open("employees.json") as file:
        data = json.load(file)

    while True:
        console.print(Panel(
            "[bold cyan]1.[/bold cyan] Login\n"
            "[bold cyan]2.[/bold cyan] Forget Password\n"
            "[bold cyan]3.[/bold cyan] Exit",
            title="[bold]Employee Access[/bold]",
            border_style="cyan"
        ))
        choice = Prompt.ask("Choose an option", choices=["1", "2", "3"])

        if choice == "1":
            emplyee_id = Prompt.ask("Employee ID (Enter 0 to back)").strip()
            if emplyee_id == "0":
                continue
            password = Prompt.ask("Password (Enter 0 to back)").strip()
            if password == "0":
                continue

            with console.status("[bold yellow]Checking credentials...[/bold yellow]"):
                time.sleep(0.6)  # small delay so the spinner is visible

            for i in data["employees"]:
                if i["employee_id"] == emplyee_id and i["password"] == password:
                    console.print(f"[bold green]Welcome Mr {i['name']}![/bold green]")
                    return project.Officer(i['name'], i['employee_id'])
            console.print("[bold red]Invalid ID or Password[/bold red]")

        elif choice == "2":
            emplyee_id = Prompt.ask("Employee ID (Enter 0 to back)").strip()
            if emplyee_id == "0":
                continue
            with open("employees.json") as file:
                data = json.load(file)
                found_employee = None
            for i in data["employees"]:
                if i["employee_id"] == emplyee_id:
                    found_employee = i
                    break
            if found_employee is None:
                console.print("[bold red]Employee Id not found.[/bold red]")
                continue

            otp = random.randint(10000, 90000)
            email = "moatazarafat223@gmail.com"
            email_password = "kgsporkpjiaalzpm"

            with console.status("[bold yellow]Sending OTP email...[/bold yellow]"):
                connection = smtplib.SMTP(host="smtp.gmail.com", port=587)
                connection.starttls()
                connection.login(user=email, password=email_password)
                connection.sendmail(
                    from_addr=email,
                    to_addrs=found_employee["email"],
                    msg=f"Subject:OTP Number\n\n{otp}"
                )
                connection.close()

            try:
                confirm = int(Prompt.ask("Enter confirm OTP"))
            except ValueError:
                console.print("[bold red]Invalid OTP format.[/bold red]")
                continue

            if otp == confirm:
                console.print("[bold green]It is correct[/bold green]")
                console.print("Update your password")
                new_password = Prompt.ask("Enter the new password")
                confirm_new_password = Prompt.ask("Confirm the new password")
                if new_password == confirm_new_password:
                    console.print("[bold green]You updated your password[/bold green]")
                    found_employee["password"] = new_password
                    with open("employees.json", "w") as file:
                        json.dump(data, file, indent=4)
                else:
                    console.print("[bold red]It is not matching[/bold red]")
            else:
                console.print("[bold red]Invalid OTP[/bold red]")

        elif choice == "3":
            return None


def vaild_country(country):
    with open("countries.txt") as file:
        for i in file:
            if i.strip().lower() == country:
                return True
    return False


# =========================================================================
# OPTION 1: Process a new traveler
# =========================================================================
def process_traveler(officer, database):
    name = Prompt.ask("Name")
    try:
        age = float(Prompt.ask("Age"))
    except ValueError:
        console.print("[bold red]Invalid age.[/bold red]")
        return
    country = Prompt.ask("Your country").lower()
    if vaild_country(country):
        console.print(f"[green]{country.title()} is a vaild country[/green]")
    else:
        console.print(f"[red]{country.title()} is not a vaild country[/red]")

    ask_passport = Prompt.ask("Has passport?", choices=["yes", "no"]).lower()
    if ask_passport == "no":
        passport = None
    else:
        passport_number = Prompt.ask("Passport number").strip()
        issue_country = Prompt.ask("Issue country").strip().lower()
        if vaild_country(issue_country):
            console.print(f"[green]{issue_country} is a vaild country[/green]")
            expiry_date = Prompt.ask("Expiry date (YYYY-MM-DD)").strip()
            passport = project.Passport(passport_number, issue_country, expiry_date)
        else:
            console.print(f"[red]{issue_country} is not a vaild country[/red]")
            passport = None

    ask_visa = Prompt.ask("Has Visa?", choices=["yes", "no"]).lower()
    if ask_visa == "no":
        visa = None
    else:
        visa_type = Prompt.ask("Visa type").strip()
        visa_country = Prompt.ask("Visa country").strip().lower()
        visa_expiry_date = Prompt.ask("Visa date (YYYY-MM-DD)").strip()
        if vaild_country(visa_country):
            console.print(f"[green]{visa_country} is a vaild country[/green]")
            visa = project.Visa(visa_type, visa_expiry_date, visa_country)
        else:
            console.print(f"[red]{visa_country} is not a vaild country[/red]")
            visa = None

    traveler = project.Traveler(name, age, country, passport, visa)

    with console.status("[bold yellow]Inspecting passport...[/bold yellow]"):
        time.sleep(0.5)
    officer.inspect_passport(traveler)

    with console.status("[bold yellow]Inspecting visa...[/bold yellow]"):
        time.sleep(0.5)
    officer.inspect_visa(traveler)

    status, reason = officer.check_entry(traveler, database.wanted_list)

    # color the final decision based on the outcome
    status_colors = {"Allowed": "green", "Rejected": "yellow", "Arrested": "red"}
    color = status_colors.get(status, "white")

    console.print(Panel(
        f"[bold]Status[/bold] : [{color}]{status}[/{color}]\n"
        f"[bold]Reason[/bold] : {reason}",
        title="Final Decision",
        border_style=color
    ))

    database.save_data(traveler, status, reason)


# =========================================================================
# OPTION 2: View the wanted list
# =========================================================================
def view_wanted_list(database):
    # EDIT: fixed - now calls the real method on the real instance
    # (database.wanted_list), instead of an unbound class method call
    # with the wrong object passed in as 'self'.
    people = database.wanted_list.wanted_people
    if len(people) == 0:
        console.print("[yellow]Wanted list is empty.[/yellow]")
        return

    table = Table(title="Wanted List", box=box.ROUNDED, border_style="red")
    table.add_column("Name", style="bold")
    table.add_column("Passport Number")
    table.add_column("Crime", style="red")

    for person in people:
        table.add_row(person["name"], person["passport_number"], person["crime"])

    console.print(table)


# =========================================================================
# OPTION 3: Add / update a person in the wanted list
# =========================================================================
def manage_wanted_list(database):
    console.print(Panel(
        "[bold cyan]1.[/bold cyan] Add new wanted person\n"
        "[bold cyan]2.[/bold cyan] Update existing wanted person\n"
        "[bold cyan]3.[/bold cyan] Back",
        border_style="cyan"
    ))
    choice = Prompt.ask("Choose an option", choices=["1", "2", "3"])

    if choice == "1":
        pass_num = Prompt.ask("Passport number").strip()
        name = Prompt.ask("Name").strip()
        crime = Prompt.ask("Crime").strip()
        database.wanted_list.add_person(pass_num, name, crime)
        # EDIT: fixed - save the WANTED LIST to disk, not database.save_data()
        # (which is for saving traveler operations and needs completely
        # different arguments: traveler, status, reason).
        database.wanted_list.save_to_file()

    elif choice == "2":
        new_pass_num = Prompt.ask("Passport number").strip()
        new_name = Prompt.ask("Name").strip()
        new_crime = Prompt.ask("Crime").strip()
        database.update_wanted(new_pass_num, new_name, new_crime)

    elif choice == "3":
        return


# =========================================================================
# OPTION 4: View daily report and statistics
# =========================================================================
def view_reports(report):
    if len(report.operations) == 0:
        console.print("[yellow]No Operations Today[/yellow]")
        return

    table = Table(title="Daily Report", box=box.ROUNDED, border_style="cyan")
    table.add_column("Name", style="bold")
    table.add_column("Passport")
    table.add_column("Status")
    table.add_column("Reason")
    table.add_column("Time", style="dim")

    status_colors = {"Allowed": "green", "Rejected": "yellow", "Arrested": "red"}

    for op in report.operations:
        color = status_colors.get(op["status"], "white")
        table.add_row(
            op["name"], op["passport"],
            f"[{color}]{op['status']}[/{color}]",
            op["reason"], op["time"]
        )

    console.print(table)

    allowed = sum(1 for op in report.operations if op["status"] == "Allowed")
    rejected = sum(1 for op in report.operations if op["status"] == "Rejected")
    arrested = sum(1 for op in report.operations if op["status"] == "Arrested")

    stats_table = Table(title="Statistics", box=box.SIMPLE)
    stats_table.add_column("Metric")
    stats_table.add_column("Count", justify="right")
    stats_table.add_row("Total Operations", str(len(report.operations)))
    stats_table.add_row("[green]Allowed[/green]", str(allowed))
    stats_table.add_row("[yellow]Rejected[/yellow]", str(rejected))
    stats_table.add_row("[red]Arrested[/red]", str(arrested))
    console.print(stats_table)

    with console.status("[bold yellow]Generating final report file...[/bold yellow]"):
        report.generate_final_report()


# =========================================================================
# MAIN MENU LOOP
# =========================================================================
def running():
    officer = login()

    if officer is None:
        console.print("[bold]Program finished successfully.[/bold]")
        return

    with console.status("[bold yellow]Loading wanted list...[/bold yellow]"):
        database = project.Database(wanted_people=[])
        database.wanted_list.load_data()
        time.sleep(0.4)

    while True:
        console.print(Panel(
            "[bold cyan]1.[/bold cyan] Process new traveler\n"
            "[bold cyan]2.[/bold cyan] View wanted list\n"
            "[bold cyan]3.[/bold cyan] Add/Update wanted person\n"
            "[bold cyan]4.[/bold cyan] View daily report and statistics\n"
            "[bold cyan]5.[/bold cyan] Exit",
            title="[bold magenta]Border Control Management System[/bold magenta]",
            border_style="magenta"
        ))
        choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4", "5"])

        if choice == "1":
            process_traveler(officer, database)
        elif choice == "2":
            view_wanted_list(database)
        elif choice == "3":
            manage_wanted_list(database)
        elif choice == "4":
            view_reports(database.report)
        elif choice == "5":
            console.print("[bold]Program finished successfully.[/bold]")
            break


if __name__ == "__main__":
    running()