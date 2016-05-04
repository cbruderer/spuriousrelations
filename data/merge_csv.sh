array=(africa allah apple arab asylum attack banana birds bitcoin black boston christian climate coffee comet crimea crowded curiosity divorce doomsday ebola epidemic ethiopia europe facebook family flu foreigners galaxy geneva gluten god google guinea higgs holidays homework hurricane immigration influenza iphone isis islam italy jogging left leone liberia linux london mandela marathon marriage maya meat mh17 mh370 migrants nelson nsa obama olympics pasta pc philippines pig pope putin refugees right rosetta russia sandy school sierra snowden sochi sports spring swine syria tea teacher television terrorism twitter ukraine unemployment unhcr usa vaccine vegan vegetarian virus watch wedding whatsapp white who work)
months=(05 06 07 09 10 11 12)

for a in ${array[@]}; do
	rm ${a}.csv
	touch ${a}.csv

	for month in ${months[@]}; do
		cat ${a}_${month}.csv >> ${a}.csv
		mv ${a}_${month}.csv deprecated/
	done
done
