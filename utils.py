from datetime import datetime

def validate_amount(amount):
  # check, if the amount is a number
  try:
    amount = float(amount)
  except ValueError:
    raise ValueError("Please enter a number")

# check, if the amount is over 0
  if amount <=0:
    raise ValueError("Amount must be over 0")

  return amount

def validate_description(description):
  # description cannot be empty
  if description.strip() == "":
    raise ValueError("Description cannot be empty")

  return description

def validate_category(category):
  # category cannot be empty
  if category.strip() == "":
    raise ValueError("Category cannot be empty")

  return category

def validate_date(date):
  # check, if date has the right format
  try:
    datetime.strptime(date, "%Y-%m-%d")
  except ValueError:
    raise ValueError("Date has to be the right format")

  return date
