DECLARE
    countvar NUMBER DEFAULT 0;
    random_seed INTEGER := to_number(to_char(systimestamp,'yyyymmdd'));
    res INTEGER := 0;
BEGIN

    SELECT COUNT(*) INTO countvar FROM MyTable;
    IF (countvar != 0)
    THEN
        DBMS_OUTPUT.put_line('There is some elements in table');
    ELSE
        FOR i IN 1..50 LOOP
            res := dbms_random.value(0, 40000);
            INSERT INTO MyTable(val) VALUES (res);
        END LOOP;
    END IF; 
END;