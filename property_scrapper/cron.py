from property_scrapper.management.commands.scrapping_script import Command

def my_scheduled_job():
  Command.handle({})
