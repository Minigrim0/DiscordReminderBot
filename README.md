# BERT

a Bot Excelling in Reminding Things

[![DeepSource](https://deepsource.io/gh/TeamNameBE/BERT.svg/?label=active+issues&show_trend=true&token=DdW16C2CB_tWuIDNbxXRm3Lw)](https://deepsource.io/gh/TeamNameBE/BERT/?ref=repository-badge)

## Supported Commands

- **/addreminder** date(jj/mm/yyy) hour(HH:MM) name(no space) duration(HH:MM) peopletoremind(@role)
  - creates a reminder at the given date that concerns the mentionned role/user
- **/delreminder** name
  - deletes a reminder
- **/modreminder** name parameter(name|start_date|duration|channel|allow_dp) new_value
  - Modifies the given field of a reminder
- **/getfuture** [hours|days|weeks] value
  - Returns the reminders until the given date (defaults to next week)
- **/help** [command]
  - displays help message about the specified command, or about every command
- **/deathping** [@someone]
  - Deathping someone (May be multiple people)
- **/stopping** [@someone]
  - Stops a deathping on someone
- **/morsty**
  - ? ? ?
- **/pic** keywords
  - Returns a random picture corresponding to the give keywords
- **/vote** "Question" "proposition 0" ... "proposition 10"
  - Creates an embed message for a quick vote

## Installation

For development purpose :

```
./setup.sh -d
```

For deployment purpose :

```
./setup.sh
```
