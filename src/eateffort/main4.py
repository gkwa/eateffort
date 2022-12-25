import datetime

import durationpy

delta = datetime.timedelta(days=365, hours=10, minutes=100)
relative = durationpy.to_str(delta, extended=True)
print(relative)
