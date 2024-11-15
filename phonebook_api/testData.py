######################################
#TEST CASES FROM REQUIREMENT
valid_phones = [
    "12345",
    "(703)111-2121",
    "123-1234",
    "+1(703)111-2121",
    "+32 (21) 212-2324",
    "1(703)123-1234",
    "011 701 111 1234",
    "12345.12345",
    "011 1 703 111 1234",
    "22.22.22.22",
    "2222.2222",
    "111 111 1111",
    "(670)123-4567",
    "670-123-4567",
    "1-670-123-4567",
    "1(670)123-4567",
    "670 123 4567",
    "670.123.4567",
    "1 670 123 4567",
    "1.670.123.4567",
]


invalid_phones = [
    "123",                       
    "1/703/123/1234",             
    "Nr 102-123-1234",            
    '<script>alert("XSS")</script>', 
    "7031111234",                
    "+1234 (201) 123-1234",       
    "(001) 123-1234",             
    "+01 (703) 123-1234",         
    "(703) 123-1234 ext 204",      
    "select * from users;" 
]


valid_names = [
    "Bruce Schneier",
    "Schneier, Bruce",
    "Schneier, Bruce Wayne",
    "O’Malley, John F.",
    "John O’Malley-Smith",
    "Cher"
]


invalid_names = [
    "Ron O’’Henry",                  
    "Ron O’Henry-Smith-Barnes",       
    "L33t Hacker",                    
    '<script>alert("XSS")</script>',  
    "Brad Everett Samuel Smith",      
    "select * from users;",            
    '<script>alert("XSS")</script>'
]


######################################
#EXTRA TEST CASES
valid_phones2 = [
    "(123) 456-7890",
    "202.555.0188",
    "123 456 7890",
    "1-800-555-5555",
    "1 (800) 555-5555",
    "+1-800-555-5555",
    "1-700-555-5555",
    "+1 415-555-2671",
    "+1 (949) 555-2671",
    "+27 21 555 5555",
    "12345-12345",
    "+1 (650) 555-3456",
    "+7 495 123-4567",
    "+1-650-555-1234",
    "+1 212 555 1234",
    "+1 646 555 4567",
    "(555) 123-4567",
]


invalid_phones2 = [
    "12",
    "1234/567",
    "555-555-55555",
    "(123)-456-789",
    "+(123) 456-7890",
    "(123)-456/7890",
    "555-555-555a",
    "+123 (456) 789 12345",
    "01112345678901",
    "+01 (800) 555-1234",
    "(000) 555-1234",
    "(123) 555 12345",
    "555-555-555",
    "555.555.555a",
    "555*555*5555",
    "+1 (123) 555_1234",
    "(555)123-456",
    "(12345) 123-1234",
    "123-1234-1234",
    "555 555 555",
    "555 555 5555 555",
    "555-555 555",
    "555-5555555",
    "555.555555",
    "555..555.5555",
    "555.5555.555",
    "(555 555-5555 ext)",
    "555-555-555 ext",
    "555-555-5555 ext123456",
    "555-555-5555x",
    "+1 (555) 555 555a",
    "1-800 555 555",
    "+1 (555) 555 555a",
    "(555) 555-5555 x99999",
    "+1 (123) 555 12a4",
    "123-123-12345",
    "+1 (123) 555-555555",
    "(123) 555 12a4",
    "+1-555-5555-1234",
    " ",
]



valid_names2 = [
    "Ann Marie",
    "Anne O’Hara",
    "Patrick O'Connor",
    "John F. Kennedy",
    "A.J. Abrams",
    "Saoirse Ronan",
    "Michael O’Leary",
    "Sir Isaac Newton",
    "Alexander Graham Bell",
    "Barack Obama",
    "Elon Musk",
    "Tim Berners-Lee",
    "William R. Hearst",
    "Serena O'Connell",
    "O’Brian, Lisa",
    "Van Helsing",
    "O’Connell, John P.",
    "Patricia O'Malley",
    "James O'Shea",
    "John O'Kelly",
    "Lara Croft",
    "Elizabeth Bennet",
    "Sherlock Holmes",
    "Dwayne O'Neil",
    "Patrick O’Doyle",
    "O’Brien, Michael J.",
    "Hugh O'Malley",
    "O’Sullivan, Liam",
    "Samantha O’Neal",
    "Santiago O’Rourke",
    "Patricia O'Reilly",
    "Catherine O'Donoghue",
    "O’Toole, Bryan",
    "Gordon O’Reilly",
    "Jessica O’Connor",
    "Bridget O’Carroll",
    "Jean O’Rourke",
    "Claire O'Malley"
]


invalid_names2 = [
    " ",
    "12345",                            
    "John123",                          
    "O’123Malley",                      
    "Jean-Luc Pic@rd",                  
    "Marie$$$Claire",                   
    "Anne O’’Connor",                   
    "Patrick O'Connor-Smith-Jones",     
    "<script>alert('XSS')",             
    "Michael O’Leary123",               
    "FitzGer@ld",                       
    "John O''''Malley",                 
    "Marie-Ann-Pierre",                 
    "Jean-Luc Picard-Dupont-Baker",     
    "O'Malley, John Paul Smith",        
    "John O''''"
]



