'''
Created on Aug 6, 2013

@author: heather
'''
import csv
from trait import*
from Bio.Seq import Seq
from Bio.Alphabet import generic_dna

class Phenotype:
    
    traits = dict() #actual traits of this genotype
    
    possibleTraitsList = [] #various possible traits
    possibleTraits = dict()


        
    def loadPossibleSNPs(self, filename):
        #load a CSV of SNPs -> traits 
        print "reading  data from " + filename 
        reader = csv.reader(open(filename, "rU"), delimiter=',')
        for row in reader:
            #print row
            if (len(row) >= 8):
                if row[0] == '':
                    continue
                
                if self.possibleTraits.has_key(row[0]):
                    trait = self.possibleTraits[row[0]]
                else:
                    trait = Trait(row[0], row[-1])
                    
                i=1
                while i< (len(row)-1):
                    trait.addAllele(row[i], row[i+1]) 
                    i=i+1
                
                self.possibleTraits[trait.rsid] = trait #add this new trait to dict indexed by RSID
                self.possibleTraitsList.append(trait) #add to list of traits as well
                #print trait
            else:
                print "row of incorrect length" , row
                
        print "done reading possible SNPs\n"
        
    def mapGenoToPheno(self, genotype):
        #for each possible trait see if we have a genotype
        #if we do add it with its value to the traits dict
        for trait in self.possibleTraitsList:
            if genotype.has_key(trait.rsid):
                self.traits[trait.rsid] = genotype[trait.rsid]
                if trait.alleles.has_key(genotype[trait.rsid]):
                    print trait.rsid, " - ", genotype[trait.rsid], " - ", trait.alleles[genotype[trait.rsid]]
                # if not try flipping the order of the alleles
                elif trait.alleles.has_key(genotype[trait.rsid][::-1]):
                     print trait.rsid, " - ", genotype[trait.rsid][::-1], " (flipped) - ", trait.alleles[genotype[trait.rsid][::-1]]
                else:
                    #try reverse complement
                    #print genotype[trait.rsid]
                    my_dna = Seq(genotype[trait.rsid], generic_dna)
                    rev = str(my_dna.complement())
                    #print rev
                    if trait.alleles.has_key(rev):
                        print trait.rsid, " - ", rev, " (rev comp) -", trait.alleles[rev]
                    # if not try flipping the order of the alleles
                    elif trait.alleles.has_key(rev[::-1]):
                        print trait.rsid, " - ", rev[::-1], " (flipped) - ", trait.alleles[rev[::-1]]
                    else:
                        print "genotype " , genotype[trait.rsid], "and rev comp " , rev, " not found in traits for " , trait.rsid   
                        
            else:
               # print trait, " genotype not found for ", trait.rsid, " available genotype mappings: ", trait.alleles
                print "genotype not found for ", trait.rsid