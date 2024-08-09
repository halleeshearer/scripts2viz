# scripts2viz
A tool to visualize the flow of inputs, outputs, and functions within scripts.

## Instructions:
- Copy scripts2viz.py and .github/workflows/update_readme_vis.yml to your directory
- Edit scripts2viz.py to change parameters at the top of the script if necessary
- Any commits made to the repo should then trigger the workflow to update the README.md file's visualization

```mermaid
 %%{init: {'theme':'base', 'themeVariables': {
  'primaryColor': '#ffcaca',
  'primaryTextColor': '#000',
  'primaryBorderColor': '#000000',
  'lineColor': '#000000',
  'tertiaryColor': '#fff'
}}}%%
graph TD
classDef lightRed fill:#ffcaca,stroke:#333,stroke-width:2px;
classDef lightGreen fill:#ebfcda,stroke:#333,stroke-width:2px;
classDef lightBlue fill:#cefbfb,stroke:#333,stroke-width:2px;
classDef lightPurple fill:#f8aaf8,stroke:#333,stroke-width:2px;

subgraph Legend
    direction TB
    key1[<b>Input]:::lightRed
    key2[<b>Function]:::lightGreen
    key3[<b>Output]:::lightBlue
    key4[<b>Intermediate</b><br> Both an input and output]:::lightPurple
end
go_to_seattle(("go_to_seattle")):::lightGreen
go_to_seattle(("go_to_seattle
 fa:fa-code"))
me:::lightRed
me --> go_to_seattle
airplane:::lightRed
airplane --> go_to_seattle
me_in_seattle:::lightBlue
go_to_seattle --> me_in_seattle
attend_neurohack(("attend_neurohack")):::lightGreen
attend_neurohack(("attend_neurohack
 fa:fa-code"))
me_in_seattle --> attend_neurohack
other_attendees:::lightRed
other_attendees --> attend_neurohack
new_friends:::lightBlue
attend_neurohack --> new_friends
new_knowledge:::lightBlue
attend_neurohack --> new_knowledge
plot_effect_map(("plot_effect_map")):::lightGreen
plot_effect_map(("plot_effect_map
 fa:fa-code"))
new_friends --> plot_effect_map
good_food:::lightRed
good_food --> plot_effect_map
sunshine:::lightRed
sunshine --> plot_effect_map
good_times:::lightBlue
plot_effect_map --> good_times
me:::lightRed
airplane:::lightRed
me_in_seattle:::lightPurple
other_attendees:::lightRed
new_friends:::lightPurple
new_knowledge:::lightBlue
good_food:::lightRed
sunshine:::lightRed
good_times:::lightBlue
```
