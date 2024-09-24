library(rotl)
library(tidyverse)
library(ggtree)

taxa <- tnrs_match_names(names = c('Isoodon obesulus',
                                    'Macropus rufogriseus',
                                    'Trichosurus vulpecula',
                                    'Felis catus',
                                    'Vulpes vulpes',
                                    'Oryctolagus cuniculus',
                                    'Canis lupis',
                                    'Macropus giganteus',
                                    'Tachyglossus aculeatus',
                                    'Sus scrofa',
                                    'Macropus robustus',
                                    'Dama dama',
                                    'Perameles nasuta',
                                    'Phascolarctos cinereus'))

tree <- tol_induced_subtree(ott_ids = ott_id(taxa))

# plot(tree, cex = .8, label.offset = .1, no.margin = TRUE)

plot(tree, label.offset=0.1, cex=1.5)

ggtree(tree)
