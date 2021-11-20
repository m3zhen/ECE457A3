function xoverKids = myCrossoverFCN(parents, options, nvars, FitnessFcn, unused, thisPopulation)
    X = rand;
    if(X <= 0.6)
        xoverKids = crossoverintermediate(parents, options, nvars, FitnessFcn, unused, thisPopulation);
    else
        xoverKids = thisPopulation;
    end