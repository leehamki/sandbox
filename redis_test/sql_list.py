SELECT_QUERY = """
SELECT trvl_name, trvl_desc, trvl_score, trvl_place, trvl_group
  FROM travel_info
"""

INSERT_QUERY = """
INSERT INTO travel_info (trvl_name ,trvl_desc ,trvl_score ,trvl_place ,trvl_group) 
VALUES ('{0}', '{1}', {2}, '{3}', '{4}')
"""

UPDATE_QUERY = """
UPDATE travel_info 
    SET trvl_name = '{1}'  
       , trvl_desc = '{2}'
       , trvl_score = {3}
       , trvl_place = '{4}'
       , trvl_group = '{5}'
  WHERE seq_no = '{0}'
"""

DELETE_QUERY = """
DELETE FROM travel_info WHERE seq_no = '{0}'
"""