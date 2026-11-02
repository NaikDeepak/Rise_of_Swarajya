#!/bin/bash
# Rise of Swarajya - installer for Age of Empires II: DE on Mac (Feral).
# Copies files only. Never deletes or overwrites anything except earlier copies of these same files.
cd "$(dirname "$0")"
BASE="$HOME/Library/Application Support/Feral Interactive/Age Of Empires II/VFS/User/Games/Age of Empires 2 DE"
PROFILE=$(ls -d "$BASE"/*/ 2>/dev/null | grep -E '/[1-9][0-9]*/$' | head -1)
if [ -z "$PROFILE" ]; then
  PROFILE=$(ls -d "$BASE"/*/ 2>/dev/null | grep -E '/[0-9]+/$' | head -1)
fi
if [ -z "$PROFILE" ]; then
  echo "Could not find your AoE2 DE profile folder under:"
  echo "  $BASE"
  echo "Start the game once, then run this again."
  read -n 1 -s -r -p "Press any key to close."; exit 1
fi
SC="${PROFILE}resources/_common/scenario"
CP="${PROFILE}resources/_common/campaign"
mkdir -p "$SC" "$CP"
cp scenarios/RS*.aoe2scenario "$SC/"
cp Rise_of_Swarajya.aoe2campaign "$CP/"
echo "Installed 15 scenarios to:"; echo "  $SC"
echo "Installed campaign to:"; echo "  $CP"
echo
echo "In game: Campaigns > Custom Campaigns > Rise of Swarajya"
echo "Or a single chapter: Single Player > Skirmish > Game Mode: Scenario > RS01..."
read -n 1 -s -r -p "Press any key to close."
