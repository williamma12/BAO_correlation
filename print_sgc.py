counter = 0
with open("sgc.ini", "w") as text_file:
    print("# COrrelation function parameters\nns=202\nnmu=100\nsmax = 202.0# Tree parameters\nminPart=500\n\n\n# Job parameters\nnworkers=23\n\n# jobs --- D filename R filename prefix [noRR]\n# prefix the parameters by job (followed by anything --- the code will sort into lexical order)\n# separate by spaces, if there is an optional 4th parameter == noRR, skip the RR in this case", file=text_file)

    for x in range(1, 6):
        counter += 1
        if x > 99:
            print("job" + str(counter) + "=/global/homes/w/wma/correlation/data_south/4" + str(x) + "_data_south.xyzw /global/homes/w/wma/correlation/random_south/4" + str(x) + "_random_south.xyzw /global/homes/w/wma/correlation/calculation/result/result_south_" + str(x), file=text_file)
        elif x > 9:
            print("job" + str(counter) + "=/global/homes/w/wma/correlation/data_south/40" + str(x) + "_data_south.xyzw /global/homes/w/wma/correlation/random_south/40" + str(x) + "_random_south.xyzw /global/homes/w/wma/correlation/calculation/result/result_south_" + str(x), file=text_file)
        else:
            print("job" + str(counter) + "=/global/homes/w/wma/correlation/data_south/400" + str(x) + "_data_south.xyzw /global/homes/w/wma/correlation/random_south/400" + str(x) + "_random_south.xyzw /global/homes/w/wma/correlation/calculation/result/result_south_" + str(x), file=text_file)
