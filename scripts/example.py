from liveodds import Odds

def main():

    odds = Odds()


    # individual race
    race = odds.race('17:00')

    print('Runners')
    for runner in race:
        print()
        print(runner['name'])

        for bookie in runner['odds']:

            print(runner['odds'][bookie])


    # get list of meetings
    meets = odds.list_meetings()
    print()
    print('Meetings:')
    print(meets)
    print()


    # print list of races for each meeting
    for meet in meets:
        print(f'Races from {meet}: ')
        print(odds.list_races(meet))
        print()


    # some data
    race = odds.list_races()[0]

    for runner in odds.race(race):
        print(f'No: {runner["number"]}  {runner["name"]}  Jockey: {runner["jockey"]}  Form: {runner["form"]}')

        for bookie in runner["odds"]:
            print(f'{bookie}: {runner["odds"][bookie]["price"]} @ {runner["odds"][bookie]["time"]}')

        print()
        


    # full meeting
    naas_races = odds.meeting('naas')

    for race in naas_races:
        for runner in naas_races[race]:
            name = runner['name']
            best_odds = runner['best_odds']['price']
            bookie = runner['best_odds']['bookie']
            print(f'Best odds for {name} in the {race}: {best_odds} with {bookie}')

        print()


if __name__ == '__main__':
    main()