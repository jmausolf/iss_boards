####################################
## Load SOURCE
####################################

source("analysis_source_cycle.R")

dfb <- dfb %>% 
  mutate(id = row_number()) %>% 
  mutate(lnyear = log(year)) %>% 
  mutate(ticker_id = as.numeric(factor(ticker))) %>%
  mutate(lnticker = log(ticker_id)) %>% 
  mutate(lnage_med = log(age_median)) %>% 
  mutate(sector2 = fct_recode(sector,
                              "Other"   = "Conglomerates",
                              "Other"   = "Consumer Goods")) %>% 
  mutate(sector2 = factor(sector2))




####################################
## Make Descriptive Stats Tables
####################################


# define the markup language we are working in.
options(qwraps2_markup = "latex") 


#Method for Total Observations
total_observations <- 
  list(
    "Observations" =
      list("N" = ~ n_distinct(.data$id),
           "Firms" = ~ n_distinct(.data$ticker),
           "Sectors" = ~ n_distinct(.data$sector),
           "Years" = ~ n_distinct(.data$year),
           "Lag Years" = ~ n_distinct(.data$lag_years)
           
      ),
    
    "Time Period and Lags" = 
      list("Year Range" = ~ paste(range(.data$year), collapse = ", "),
           "Years Included (w/lag)" = ~ paste(min(.data$year)-min(.data$lag_years), max(.data$year), sep = ", "),
           "Lag Range" = ~ paste(range(.data$lag_years), collapse = ", ")
      )
  )





total_board_change <-
  list(
    "New Board Members" =
      list("Republicans" = ~ n_perc(.data$new_bm_party_rep == 1, na_rm = TRUE, show_denom = "never"),
           "Democrats" = ~ n_perc(.data$new_bm_party_dem == 1, na_rm = TRUE, show_denom = "never"),
           "Unknown" = ~ n_perc(.data$new_bm_party_unk== 1, na_rm = TRUE, show_denom = "never")
      ),
    
    "Dropped Board Members" =
      list("Republicans" = ~ n_perc(.data$dropped_bm_party_rep == 1, na_rm = TRUE, show_denom = "never"),
           "Democrats" = ~ n_perc(.data$dropped_bm_party_dem == 1, na_rm = TRUE, show_denom = "never"),
           "Unknown" = ~ n_perc(.data$dropped_bm_party_unk == 1, na_rm = TRUE, show_denom = "never")
      )
    
  )

# board_change <- df %>% 
#   summary_table(total_board_change)



#Method for Job Types, Locations
board_events <-
  list(
    "Board Events" =
      list("Add" = ~ n_perc(.data$board_change_events_list_ADD),
           "Drop" = ~ n_perc(.data$board_change_events_list_DROP),
           "Swap" = ~ n_perc(.data$board_change_events_list_SWAP),
           "Equal Swap" = ~ n_perc(.data$equal_swap_ep_party_yes),
           "Unequal Swap" = ~ n_perc(.data$equal_swap_ep_party_no),
           "No Change" = ~ n_perc(.data$board_change_events_list_NO_CHANGE)
      )
  )

# events <- df_stats %>%
#   summary_table(board_events)

event_matching <-
  list(
    #event_match_ep_party_bp_pid2n_mean
    "Event Match" =
      list("Match" = ~ n_perc(.data$event_match_ep_party_bp_pid2n_mean_YES, na_rm = TRUE, show_denom = "never"),
           "Unmatched" = ~ n_perc(.data$event_match_ep_party_bp_pid2n_mean_NO, na_rm = TRUE, show_denom = "never"),
           "Missing" = ~ n_perc(.data$event_match_ep_party_bp_pid2n_mean_NA, na_rm = TRUE, show_denom = "never")
      )
    
  )

# events <- df_stats %>%
#   summary_table(board_events)




firm_parties <-
  list(
    "Board Party X Events" =
             list("Democratic Board" = ~ n_perc(.data$bp_pid2n_median_DEM, na_rm = TRUE, show_denom = "never"),
                  "Republican Board" = ~ n_perc(.data$bp_pid2n_median_REP, na_rm = TRUE, show_denom = "never")
             ),
    
    "Firm Party X Events" =
      list("Polarized Democratic" = ~ n_perc(.data$fec_cluster_party_DEM, na_rm = TRUE, show_denom = "never"),
           "Amphibious Firm" = ~ n_perc(.data$fec_cluster_party_OTH, na_rm = TRUE, show_denom = "never"),
           "Polarized Republican" = ~ n_perc(.data$fec_cluster_party_REP, na_rm = TRUE, show_denom = "never")
      ),
    
    "U.S. Presidential Party" =
      list("Democrat" = ~ n_perc(.data$who_pres_DEM, na_rm = TRUE, show_denom = "never"),
           "Republican" = ~ n_perc(.data$who_pres_REP, na_rm = TRUE, show_denom = "never")
      )
  )

# parties <- df_stats %>%
#   summary_table(firm_parties)

#Method for Board Stata
board_stats <-
  list(
    "Board-Level Metrics (Mean)" =
      list("Median Age" = ~ mean_sd(.data$age_median),
           "Female Proportion" = ~mean_sd(.data$female_yes_mean),
           "Black / Hispanic Proportion" = ~mean_sd(.data$aa_hisp_yes_mean),
           "Minority Proportion" = ~mean_sd(.data$minority_yes_mean),
           "Non-USA Proportion" = ~mean_sd(.data$non_usa_yes_mean),
           "Board Size" = ~mean_sd(.data$board_size),
           "Median Outside Board Ties" = ~mean_sd(.data$outside_public_boards_median)
           
      )
  )

# bm_stats <- df %>%
#     summary_table(board_stats)






#########################################
## Lag 1
#########################################

df <- dfb %>%
  filter(lag_years == 1)

#Get Board Change
board_change <- df %>% 
  summary_table(total_board_change)

#Get Board Stats
bm_stats <- df %>%
  summary_table(board_stats)

#Get Observations
observations <- df %>% 
  summary_table(total_observations)

#Make Additional Dummies
df_stats <- dummy_cols(df, select_columns = c("board_change_events_list",
                                              "fec_cluster_party",
                                              "bp_pid2n_median",
                                              "who_pres",
                                              "event_match_ep_party_bp_pid2n_mean",
                                              "event_match_ep_pid2ni_med_str_bp_pid2ni_med_mean"))
#Get Board Events
events <- df_stats %>%
  summary_table(board_events)

#Get Event Matching
event_matches <- df_stats %>%
  summary_table(event_matching)


#Get Parties
parties <- df_stats %>%
  summary_table(firm_parties)


#Combined Table for All Data
tab_l1 <- rbind(events, board_change, event_matches, bm_stats, parties, observations)
tab_l1



#########################################
## Lag 2
#########################################

df <- dfb %>%
  filter(lag_years == 2)

#Get Board Change
board_change <- df %>% 
  summary_table(total_board_change)

#Get Board Stats
bm_stats <- df %>%
  summary_table(board_stats)

#Get Observations
observations <- df %>% 
  summary_table(total_observations)

#Make Additional Dummies
df_stats <- dummy_cols(df, select_columns = c("board_change_events_list",
                                              "fec_cluster_party",
                                              "bp_pid2n_median",
                                              "who_pres",
                                              "event_match_ep_party_bp_pid2n_mean",
                                              "event_match_ep_pid2ni_med_str_bp_pid2ni_med_mean"))

#Get Board Events
events <- df_stats %>%
  summary_table(board_events)

#Get Event Matching
event_matches <- df_stats %>%
  summary_table(event_matching)

#Get Parties
parties <- df_stats %>%
  summary_table(firm_parties)


#Combined Table for All Data
tab_l2 <- rbind(events, board_change, event_matches, bm_stats, parties, observations)
tab_l2


#########################################
## Lag 2-4
#########################################

df <- dfb %>%
  filter(lag_years >= 2 & lag_years <= 4)

#Get Board Change
board_change <- df %>% 
  summary_table(total_board_change)

#Get Board Stats
bm_stats <- df %>%
  summary_table(board_stats)

#Get Observations
observations <- df %>% 
  summary_table(total_observations)

#Make Additional Dummies
df_stats <- dummy_cols(df, select_columns = c("board_change_events_list",
                                              "fec_cluster_party",
                                              "bp_pid2n_median",
                                              "who_pres",
                                              "event_match_ep_party_bp_pid2n_mean",
                                              "event_match_ep_pid2ni_med_str_bp_pid2ni_med_mean"))

#Get Board Events
events <- df_stats %>%
  summary_table(board_events)

#Get Event Matching
event_matches <- df_stats %>%
  summary_table(event_matching)

#Get Parties
parties <- df_stats %>%
  summary_table(firm_parties)


#Combined Table for All Data
tab_l2_4 <- rbind(events, board_change, event_matches, bm_stats, parties, observations)
tab_l2_4


#########################################
## Lag All
#########################################

df <- dfb 

#Get Board Change
board_change <- df %>% 
  summary_table(total_board_change)

#Get Board Stats
bm_stats <- df %>%
  summary_table(board_stats)

#Get Observations
observations <- df %>% 
  summary_table(total_observations)

#Make Additional Dummies
df_stats <- dummy_cols(df, select_columns = c("board_change_events_list",
                                              "fec_cluster_party",
                                              "bp_pid2n_median",
                                              "who_pres",
                                              "event_match_ep_party_bp_pid2n_mean",
                                              "event_match_ep_pid2ni_med_str_bp_pid2ni_med_mean"))

#Get Board Events
events <- df_stats %>%
  summary_table(board_events)

#Get Event Matching
event_matches <- df_stats %>%
  summary_table(event_matching)

#Get Parties
parties <- df_stats %>%
  summary_table(firm_parties)


#Combined Table for All Data
tab_all <- rbind(events, board_change, event_matches, bm_stats, parties, observations)
tab_all


#########################################
## Make Final Table
#########################################


final_table <- cbind(tab_l1, tab_l2, tab_l2_4, tab_all)
final_table



capture.output(print(final_table,
                     booktabs = TRUE,
                     rtitle = "Summary Statistics",
                     cnames = c("1 Year Lag", "2 Year Lag", "2-4 Year Lags", "All Year Lags")), 
               file="output/tables/table_descriptive_stats_cycle.tex")