library(tidyverse)
library(ggbump)
library(showtext)
showtext.auto()

# setwd(dirname(rstudioapi::getActiveDocumentContext()$path)) #set the wd to the current directory
# 
# df = read.csv("df.csv")
# 



 #--this value defines the number of intervals and margins

## ggplot theme
theme_set(theme_void(base_family = "arial"))

theme_update(
  axis.text.x.top = element_text(
    size = 50,
    color = "#1d3557",
    face = "bold",
    vjust = 1.5
  ),
  axis.title.x.bottom = element_text(
    color = "black", 
    size = 37, 
    face = "bold",
    vjust = -2
  ),
  plot.margin = margin(15, 30, 5, 50),
  plot.background = element_rect(
    fill = "#f5f3f4", 
    color = "grey"
  ),
  plot.caption = element_text(
    color = "#6c757d", 
    size = 25, 
    hjust = 1, 
    margin = margin(t = 15, b = 0)
  ),
  plot.caption.position = "plot"
)

#==== Function 
bump_rank <- function(df,len,type_select,OR){
month = unique(c(df$time))
state_n = length(unique(c(df$feature)))
length = length(month)
df_rank <-
  df %>% 
  dplyr::select(time, feature, counts) %>% 
  mutate(time = factor(time))%>%
  group_by(time, feature) %>% 
  summarize(points = unique(counts)) %>% 
  group_by(feature) %>% 
  arrange(feature, time) %>% 
  mutate(
    points_sum = sum(points),
    points_cum = cumsum(points)
  ) %>%
  group_by(time) %>% 
  arrange(-points) %>% 
  mutate(rank = row_number()) %>% 
  ungroup() %>% 
  mutate(
    race_num = as.numeric(time),
    team_name = fct_reorder(feature, -points)
  )

cols <- c(
  "#450920", "#0081a7", "#a53860", "#d90429", "#da627d", "#ffa5ab","#2ec4b6",  "#f9dbbd",
  "#455e89", "#2e6f95",  "#cb997e", "#FFCB69",
  "#6b705c", "#0a9396", "#577590", "#8a5a44", "#354f52", "#bee3db",
  "#4d194d", "#b21e35", "#f4845f", "#f79d65", "#87bba2",
  "#fec89a", "#bfa89e", "#736f72", "#d5c7bc", "#6f2231",
  "#02c39a", "#63647e", "#b69121", "#856a5d", "#608460",
  "#455e89", "#2e6f95", "#1780a1", "#0091ad", "#B34525",
  "#FCD306", "#9AD1E8", "#D44F4C", "#BB1A4E", "#A5C254", 
  "#882B1A", "#676564", "#E8751C",  "#646E3F",
  "#9D49B9", "#C09F2F", "#65955B", "#284D95", "#B34525",
  "#450920", "#0081a7", "#a53860", "#d90429", "#da627d", "#ffa5ab","#2ec4b6",  "#f9dbbd",
  "#455e89", "#2e6f95",  "#cb997e", "#FFCB69",
  "#6b705c", "#0a9396", "#577590", "#8a5a44", "#354f52", "#bee3db",
  "#4d194d", "#b21e35", "#f4845f", "#f79d65", "#87bba2",
  "#fec89a", "#bfa89e", "#736f72", "#d5c7bc", "#6f2231",
  "#02c39a", "#63647e", "#b69121", "#856a5d", "#608460",
  "#455e89", "#2e6f95", "#1780a1", "#0091ad", "#B34525",
  "#FCD306", "#9AD1E8", "#D44F4C", "#BB1A4E", "#A5C254", 
  "#882B1A", "#676564", "#E8751C",  "#646E3F",
  "#9D49B9", "#C09F2F", "#65955B", "#284D95", "#B34525"
)

bump <- df_rank %>% 
  ggplot(aes(
    x = race_num, 
    y = rank, 
    color = team_name,
    group = team_name
  )) +

    geom_segment(
    data = tibble(
      x = 1,
      xend = length,
      y = 1:state_n #--number of states
    ),
    aes(
      x = x, xend = xend,
      y = y, yend = y
    ),
    color = "white",
    size = .15,
    inherit.aes = FALSE
  ) +
  geom_bump(
    smooth = 20, 
    size = 2
  ) +

  geom_point(
    data = df_rank %>% filter(race_num == length),
    size = 3.5,
    stroke = 1.5
  ) +
  geom_point(
    data = df_rank,
    size = 9, 
    shape = 21, 
    fill = "#f5f3f4",
    stroke = 1.5
  ) +
  geom_text(
    data = df_rank %>% filter(race_num == 1),
    aes(x =0.27,
      label = feature
    ),
    family = "Arial",
    size = 16,
    inherit.aes = TRUE,
    hjust=0
  ) +
  geom_text(
    data = df_rank %>% filter(race_num == 1),
    aes(x =0.82,
        label = rank
    ),
    family = "Arial",
    size = 15,
    inherit.aes = TRUE,
    hjust=1) +
  geom_text(
    data = df_rank %>% filter(race_num == length),
    aes(
      x = length + 0.15,
      label = feature
    ),
    family = "arial",
    size = 16,
    hjust = 0
  )+
  geom_text(
    data = df_rank %>% filter(race_num == length),
    aes(
      x = length + 0.68,
      label = rank
    ),
    family = "Arial",
    face = "bold",
    size = 15,
    hjust = 1
  ) +
  coord_cartesian(clip = "off") +
  scale_x_continuous(
    expand = c(.001, .001),
    limits = c(0.2, length+.7),
    breaks = 1:length,
    labels = month,
    sec.axis = dup_axis()
  ) +
  scale_y_reverse(
    expand = c(.03, .03),
    breaks = 1:22
  ) +
  scale_color_manual(
    values = cols,
    guide = F
  ) +
  labs(
    x = glue::glue_col("This will be changed (placeholder for the main title of this figure)"),
    caption = ""
  ) 

for (i in len:1){
  print (i)
  bump <- bump + geom_text(
    data = df_rank %>% filter(race_num == i),
    aes(x =!!(i-.02),  #the ii will remove the lazy evaluation of ggplot (when using for loops)
        label = points
    ),
    family = "Arial",
    size = 13,
    inherit.aes = TRUE,
    hjust=0
  )
}

if (!OR){
if (type_select=='All'){ h_max = state_n-(state_n/2)-.75
w = length+7}
else if(type_select=='DIAG-ICD10') {h_max = state_n-(state_n/2)-2
w = length+5}
else if(type_select=='MED-CLASS') {h_max = state_n-(state_n/2)+3
w = length+5}
else if(type_select=='LAB-LOINC') {h_max = state_n-(state_n/2)+3
w = 6}
else {h_max = 3.5
w = length+5}
}

else{h_max= 3.75
w = length+5}

ggsave("Images/rank.jpeg", width = w, height = h_max)

}


# bump_rank(df,4)

