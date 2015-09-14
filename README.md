Installation and set up for De_Mo:

Make sure config file gets set
`export DE_MO_SETTINGS=/Users/SBurns/code/de_mo`

Pipe the schemal into the sqlite3 DATABASE (make sure you have the path correct)
`sqlite3 /tmp/de_mo.db < schema.sql`
