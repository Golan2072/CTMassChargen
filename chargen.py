#chargen.py
#classic traveller mass character generator
#version 0.1.2 - June 7th, 2024
#by Omer Golan-Joel golan2072@gmail.com
#open source under the Creative Commons Zero 1.0 License

import utility
import json
import random

blade_list = ["Blade", "Cutlass", "Sword", "Broadsword", "Polearm", "Cudgel", "Spear", "Dagger"]
gun_list = ["Autopistol", "SMG", "Rifle", "Body Pistol", "Autorifle", "Carbine", "Revolver", "Shotgun", "Laser Carbine", "Laser Rifle"]
vehicle_list = ["Ground Car", "ATV", "AFV", "G-Carrier", "Air/Raft", "Speeder", "Motorboat", "Submersible", "Biplane", "Jump Jet"]

def stat_roll_parser(stat_string):
    stat_name = str(stat_string[:3])
    threshold = stat_string[3]
    stat_list = ["STR", "DEX", "END", "INT", "EDU", "SOC"]
    return [int(stat_list.index(stat_name)), int(threshold)] #returns UPP stat index and threshold

def add_skill(skill_dict, skill):
    if skill == "Blade Combat":
        skill = random.choice(blade_list)
    elif skill == "Gun Combat":
        skill = random.choice(gun_list)
    elif skill == "Vehicle":
        skill = random.choice(vehicle_list)
    if skill not in skill_dict:
        skill_dict[skill] = 1
    elif skill in skill_dict:
        skill_dict[skill] += 1
    else:
        pass
    return skill_dict

def inventory_check (item, skills):
    if item == "Gun":
        for skill in skills:
            if skill in gun_list:
                item = skill
            else:
                item = random.choice(gun_list)
        else:
            pass
    elif item == "Blade":
        for skill in skills:
            if skill in blade_list:
                item = skill
            else:
                item = random.choice(blade_list)
    elif item == "Vehicle":
        for skill in skills:
            if skill in vehicle_list:
                item = skill
            else:
                item = random.choice(vehicle_list)
    else:
        pass
    return item

def add_item(inventory, item, skills):
    item = inventory_check (item, skills)
    if item not in inventory:
        inventory[item] = 1
    elif item in inventory:
        inventory[item] += 1
    else:
        pass
    return inventory

def survival(char_data, career, upp):
        survival_roll = utility.dice(2, 6)
        modifier = stat_roll_parser(char_data[career]['survival+2'])
        if int(upp[[modifier][0][0]]) >= int([modifier][0][1]):
            survival_roll += 2
        if survival_roll >= char_data[career]["survival"]:
            survival = True
        else:
            survival = False
        return survival

def commission (char_data, career, upp):
        if char_data[career]['commission+1'] == "":
            return False
        else:
            commission_roll = utility.dice(2, 6)
            modifier = stat_roll_parser(char_data[career]["commission+1"])
            if int(upp[[modifier][0][0]]) >= int([modifier][0][1]):
                commission_roll +=1
            if commission_roll >= int(char_data[career]["commission"]):
                return True
            else:
                return False
            
def promotion (char_data, career, upp, rank):
        if char_data[career]['promotion+1'] == "":
            return False
        else:
            promotion_roll = utility.dice(2, 6)
            modifier = stat_roll_parser(char_data[career]["promotion+1"])
            if int(upp[[modifier][0][0]]) >= int([modifier][0][1]):
                promotion_roll += 1
            if promotion_roll >= int(char_data[career]["promotion"]):
                rank += 1
                return rank, True
            else:
                return rank, False
            

class Character:
    def __init__(self, library_file, death):
        library = open(library_file) #library_file being a .json file
        self.char_data = json.load(library)
        self.career_list = []
        for career in self.char_data:
            self.career_list.append(career)
        if utility.dice(1,6) <= 3:
            self.name = utility.random_line("Data/malenames.txt") + " " + utility.random_line("Data/surnames.txt")
            self.sex = "Male"
        else:
            self.name = utility.random_line("Data/femalenames.txt") + " " + utility.random_line("Data/surnames.txt")
            self.sex = "Female"
        self.upp = [utility.dice(2, 6), utility.dice(2, 6), utility.dice(2, 6), utility.dice(2, 6), utility.dice(2, 6), utility.dice(2, 6)]
        self.career_choice()
        self.enlistment ()
        self.rank = 0
        self.skills = {}
        self.skill_string = ""
        self.upp_string = ""
        self.inventory_string = ""
        self.char_string = ""
        self.species = "Human"
        self.status = "Alive"
        self.rank_text = ""
        self.inventory = {}
        i = 0
        self.terms = 0
        self.cash = 0
        self.age = 18
        if "0" in self.char_data[self.career]["autoskills"]:
            self.skills = add_skill(self.skills, self.char_data[self.career]["autoskills"]["0"])
        while True:
            self.terms += 1
            self.age += 4
            survival_margin = survival(self.char_data, self.career, self.upp)
            if survival_margin == True:
                self.status = "alive"
            elif survival_margin == False and death == True:
                self.status = "DECEASED"
                break
            self.skills = add_skill(self.skills,self.skill_roll())
            if self.terms == 1:
                self.skills = add_skill(self.skills,self.skill_roll())
            else:
                pass
            if self.rank == 0:
                commission_check = commission(self.char_data, self.career, self.upp)
                if commission_check == True:
                    self.rank = 1
                    self.skills = add_skill(self.skills,self.skill_roll())
                else:
                    self.rank = 0
            elif self.rank in range (1, 7):
                rank_check = promotion(self.char_data, self.career, self.upp, self.rank)
                if rank_check[1] == True:
                    self.rank = rank_check[0]
                    self.skills = add_skill(self.skills,self.skill_roll())
                else:
                    pass
            if str(self.rank) in self.char_data[self.career]["autoskills"]:
                if self.char_data[self.career]["autoskills"][str(self.rank)] in self.skills:
                    pass
                else:
                    self.skills = add_skill(self.skills, self.char_data[self.career]["autoskills"][str(self.rank)])
            self.aging()
            if self.terms < 7 and utility.dice(2, 6) >= self.char_data[self.career]["reenlist"] and survival(self.char_data, self.career, self.upp) == True:
                pass
            elif self.terms == 7 and utility.dice(2, 6) < 12:
                break
            elif self.terms == 8:
                break
            else:
                break
        self.mustering_out()
        characteristic_list_1 = ["STR1", "DEX1", "END1", "INT1", "EDU1", "SOC1"]
        characteristic_list_2 = ["STR2", "DEX2", "END2", "INT2", "EDU2", "SOC2"]
        characteristic_list_3 = ["STR-1", "DEX-1", "END-1", "INT-1", "EDU-1", "SOC-1"]
        for skill in self.skills.copy():
            if skill in characteristic_list_1:
                char_index = characteristic_list_1.index(skill)
                self.upp[char_index] += 1
                self.skills.pop(skill)
            if skill in characteristic_list_2:
                char_index = characteristic_list_2.index(skill)
                self.upp[char_index] += 2
                self.skills.pop(skill)
            if skill in characteristic_list_3:
                char_index = characteristic_list_3.index(skill)
                self.upp[char_index] -= 1
                self.skills.pop(skill)
        self.skill_stringer()
        self.rank_stringer()
        self.upp_stringer()
        self.inventory_stringer()
        self.char_stringer()

    def career_choice(self):
        if max(self.upp) == self.upp[0]:
            self.career = "Marines"
        elif max(self.upp) == self.upp[1]:
            self.career = random.choice(["Army", "Scouts"])
        elif max(self.upp) == self.upp[3]:
            self.career = "Merchants"
        elif max(self.upp) == self.upp[4]:
            self.career = "Navy"
        else:
            self.career = random.choice(self.career_list)

    def enlistment (self):
        enlist_roll = utility.dice(2, 6)
        if self.char_data[self.career]['enlistment+1'] == "":
            pass
        else:
            modifier_1 = stat_roll_parser(self.char_data[self.career]['enlistment+1'])
            modifier_2 = stat_roll_parser(self.char_data[self.career]['enlistment+2'])
            if int(self.upp[[modifier_1][0][0]]) >= int([modifier_1][0][1]):
                enlist_roll += 1
            if int(self.upp[[modifier_2][0][0]]) >= int([modifier_2][0][1]):
                enlist_roll += 2
            if enlist_roll >= self.char_data[self.career]["enlistment"]:
                pass
            else:
                self.career = random.choice(self.career_list)
            
    def skill_roll (self):
        if self.upp[4] >= 8:
            skill_table = random.choice (["personal", "service", "advanced", "advanced8"])
        else:
            skill_table = random.choice (["personal", "service", "advanced"])
        return random.choice(self.char_data[self.career][skill_table])

    def mustering_out (self):
        characteristic_list_1 = ["STR1", "DEX1", "END1", "INT1", "EDU1", "SOC1"]
        characteristic_list_2 = ["STR2", "DEX2", "END2", "INT2", "EDU2", "SOC2"]
        cash_count = 0
        i = 0
        while i in range (0, self.terms+1):
            i += 1
            if utility.dice(1,6) <= 3 and cash_count <= 3:
                cash_count += 1
                cash_roll = utility.dice(1,6)
                if "Gambling" in self.skills:
                    cash_roll += 1
                self.cash += self.char_data[self.career]["cash"][cash_roll-1]
            else:
                material_roll = utility.dice(1,6)
                if self.rank >= 5:
                    material_roll += 1
                add_item(self.inventory, self.char_data[self.career]["benefits"][material_roll-1], self.skills)
                for item in self.inventory.copy():
                    if item in characteristic_list_1:
                        char_index = characteristic_list_1.index(item)
                        self.upp[char_index] += 1
                        self.inventory.pop(item)
                    if item in characteristic_list_2:
                        char_index = characteristic_list_2.index(item)
                        self.upp[char_index] += 2
                        self.inventory.pop(item)
    
    def aging (self):
        if self.age >= 34 and self.age < 50:
            if utility.dice(2, 6) < 8:
                self.upp[0] -= 1
            if utility.dice(2, 6) < 7:
                self.upp[1] -= 1
            if utility.dice(2, 6) < 8:
                self.upp[2] -= 1
        elif self.age >= 50 and self.age < 66:
            if utility.dice(2, 6) < 9:
                self.upp[0] -= 1
            if utility.dice(2, 6) < 8:
                self.upp[1] -= 1
            if utility.dice(2, 6) < 9:
                self.upp[2] -= 1
        elif self.age >= 66:
            if utility.dice(2, 6) < 9:
                self.upp[0] -= 2
            if utility.dice(2, 6) < 9:
                self.upp[1] -= 2
            if utility.dice(2, 6) < 9:
                self.upp[2] -= 2
            if utility.dice(2, 6) < 9:
                self.upp[3] -= 1
        else:
            pass
        for characteristic in self.upp:
            if characteristic <= 0:
                if utility.dice(2, 6) < 8:
                    self.status = "DECEASED"
                else:
                    self.upp[characteristic] = 1
    
    def skill_stringer(self):
        for skill in self.skills:
            skill_description = skill + " " + str(self.skills[skill])
            if self.skill_string == "":
                self.skill_string = skill_description
            else:
                self.skill_string = ", ".join([self.skill_string, skill_description])
    
    def rank_stringer(self):
        self.rank_text = self.rank_text = self.char_data[self.career]["ranks"][str(self.rank)]
        if self.upp[5] == 11 and self.sex == "Male":
            self.rank_text += " Knight"
        elif self.upp[5] == 11 and self.sex == "Female":
            self.rank_text += " Dame"
        elif self.upp[5] == 12 and self.sex == "Male":
            self.rank_text += " Baron"
        elif self.upp[5] == 12 and self.sex == "Female":
            self.rank_text += " Baroness"
        elif self.upp[5] == 13 and self.sex == "Male":
            self.rank_text += " Marquis"
        elif self.upp[5] == 13 and self.sex == "Female":
            self.rank_text += " Marquesa"
        elif self.upp[5] == 14 and self.sex == "Male":
            self.rank_text += " Count"
        elif self.upp[5] == 14 and self.sex == "Female":
            self.rank_text += " Countess"
        elif self.upp[5] == 15 and self.sex == "Male":
            self.rank_text += " Duke"
        elif self.upp[5] == 15 and self.sex == "Female":
            self.rank_text += " Duchess"
        if "Medical" in self.skills:
            if self.skills["Medical"] >= 3:
               self.rank_text += " Dr."
            elif self.upp[4] >= 12 and self.upp[4] < 15:
                self.rank_text += " Dr."
            elif self.upp[4] >= 15:
                self.rank_text += " Prof."
        elif self.upp[4] >= 12 and self.upp[4] < 15:
                self.rank_text += " Dr."
        elif self.upp[4] >= 15:
                self.rank_text += " Prof."
        else:
            pass

    def upp_stringer(self):
        for digit in self.upp:
            if self.upp_string == "":
                self.upp_string = str(utility.pseudo_hex(digit))
            else:
                self.upp_string = "".join([self.upp_string, str(utility.pseudo_hex(digit))])

    def inventory_stringer(self):
        for item in self.inventory:
            final_item = item
            item_description = final_item + " x" + str(self.inventory[item])
            if self.inventory_string == "":
                self.inventory_string = item_description
            else:
                self.inventory_string = ", ".join([self.inventory_string, item_description])
    
    def char_stringer(self):
        self.char_string = f"{self.career} {self.rank_text} {self.name} {self.upp_string}   Age {self.age} {self.terms} terms Cr {self.cash}\n{self.species} {self.sex}\n{self.skill_string}\nInventory: {self.inventory_string}"

if __name__ == "__main__":
    test = Character("Data/careers.json", False)
    print (test.char_string)