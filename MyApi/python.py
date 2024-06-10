from MyApi.models import Table
from datetime import timedelta

# Create a new table instance
table = Table.objects.get(id=1)

# Start the stopwatch
table.start_stopwatch()

# Stop the stopwatch
table.stop_stopwatch()

# Get the elapsed time
elapsed_time = table.get_elapsed_time()
print(f"Elapsed time: {elapsed_time}")

# Reset the stopwatch
table.reset_stopwatch()
