# liveodds
An API for live race odds and minimal runner information

## Requirements

[Python3](https://www.python.org/downloads/) is needed with [lxml](https://lxml.de/) and [requsts](https://2.python-requests.org/en/master/) modules.

```
$ pip install lxml requests
```

## Installation
```
$ git clone https://github.com/4A47/liveodds.git
```
or download [here](https://github.com/4A47/liveodds/archive/master.zip)

<pre>
## Usage
```python
from liveodds import Odds

odds = Odds()
```
</pre>

## Methods

<pre>
#### odds.all()
Returns full JSON for all UK/IRE races
```python
races = odds.all()

for race in races:
    print(races[race])
```
</pre>

<pre>
#### odds.race(race)
Returns JSON for given individual race
```python
race = odds.race('20:50')

for runner in race:
    print(runner["number"], runner["name"], runner["jockey"], runner["form"])
    
    for bookie in runner["odds"]:
        print(bookie, runner["odds"][bookie]["price"])
```
</pre>

<pre>
#### odds.meeting(meeting)
Returns JSON for all races at a given meeting
```python
naas_races = odds.meeting('naas')

	for race in naas_races:
		for runner in naas_races[race]:
			name = runner['name']
			best_odds = runner['best_odds']['price']
			bookie = runner['best_odds']['bookie']
			print(f'Best odds for {name} in the {race}: {best_odds} with {bookie}')
```
</pre>

<pre>
#### odds.list_meetings()
Returns list of all meetings
```python
for meeting in odds.list_meetings():
    print(meeting)
```
</pre>

<pre>
#### odds.list_races(optional_meeting)
Returns list of all race times, or all from an individual meeting
```python
for time in odds.list_races():
    for runner in odds.race(time):
        print(runner["draw"])
        
for meeting in odds.list_meetings():
    for race_time in odds.list_races(meeting):
        print(odds.race(race_time))
```
</pre>