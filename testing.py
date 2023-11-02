import classes.item as i
import classes.actor as a

if __name__ == '__main__':
    item1 = i.Item()
    determined = i.determine_items()
    classes = []

    # This will be code to load items in items_list
    for item in determined:
        match item[0]:
            case "Leather":
                classes.append(i.Leather())
            case "Ring Mail":
                classes.append(i.RingMail())
            case "Studded Leather":
                classes.append(i.StuddedLeather())
            case "Scale Mail":
                classes.append(i.ScaleMail())
            case "Chain Mail":
                classes.append(i.ChainMail())
            case "Splint Mail":
                classes.append(i.SplintMail())
            case "Banded Mail":
                classes.append(i.BandedMail())
            case "Plate Mail":
                classes.append(i.PlateMail())
            case "Magic Mapping":
                classes.append(i.MagicMapping(desc=item[1]))
            case "Identify Weapon":
                classes.append(i.IdentifyWeapon(desc=item[1]))
            case "Identify Armor":
                classes.append(i.IdentifyArmor(desc=item[1]))
            case "Remove Curse":
                classes.append(i.RemoveCurse(desc=item[1]))
            case "Poison":
                classes.append(i.Poison(desc=item[1]))
            case "Monster Detection":
                classes.append(i.MonsterDetection(desc=item[1]))
            case "Restore Strength":
                classes.append(i.RestoreStrength(desc=item[1]))
            case "Healing":
                classes.append(i.Healing(desc=item[1]))
            case "Light":
                classes.append(i.Light(desc=item[1]))
            case "Teleport To":
                classes.append(i.TeleportTo(desc=item[1]))
            case "Teleport Away":
                classes.append(i.TeleportAway(desc=item[1]))
            case "Slow Monster":
                classes.append(i.SlowMonster(desc=item[1]))
            case "Add Strength":
                classes.append(i.AddStrength(desc=item[1]))
            case "Increase Damage":
                classes.append(i.IncreaseDamage(desc=item[1]))
            case "Teleportation":
                classes.append(i.Teleportation(desc=item[1]))
            case "Dexterity":
                classes.append(i.Dexterity(desc=item[1]))
            case _:
                # Will never get here
                pass

    print(f"Number of classes: {len(classes)}")
    for cls in classes:
        armors = [i.Leather, i.RingMail, i.StuddedLeather, i.ScaleMail, i.ChainMail, i.SplintMail, i.BandedMail,
                  i.PlateMail]
        if type(cls) not in armors:
            print(f"title: {cls.title}, hidden title: {cls.hidden_title}, id: {cls.id}")
        else:
            print(f"title: {cls.title}, id: {cls.id}")