DECLARE
    countvar NUMBER DEFAULT 0;
    random_seed INTEGER := to_number(to_char(systimestamp,'yyyymmdd'));
    res INTEGER := 0;
    
    PROCEDURE Analyze IS
        chet NUMBER := 0;
        nechet NUMBER := 0;
    BEGIN
        SELECT COUNT(*) INTO chet FROM MyTable WHERE MOD(val, 2) = 0;
        SELECT COUNT(*) INTO nechet FROM MyTable WHERE MOD(val, 2) = 1;
        
        IF (chet = nechet)
        THEN
            DBMS_OUTPUT.put_line('EQUAL');
        ELSE
            IF (chet > nechet)
            THEN
                DBMS_OUTPUT.put_line('TRUE (CHET)');
            ELSE
                DBMS_OUTPUT.put_line('FALSE (NECHET)');
            END IF;
        END IF;
    END;
    
    PROCEDURE GenerateInsert (inpId NUMBER) IS
        myval NUMBER := 0;
    BEGIN
        SELECT val INTO myval FROM MyTable WHERE MyTable.ID = inpId;
        
        DBMS_OUTPUT.put_line('INSERT INTO MyTable(val) VALUES (' || myval || ');');
    END;
    
    PROCEDURE MyInsert(inpval NUMBER) AS
    BEGIN
        INSERT INTO MyTable(val) VALUES (inpval);
    END;
    
    PROCEDURE MyUpdate(inpId NUMBER, inpval NUMBER)IS
    BEGIN
        UPDATE MyTable SET val = inpval WHERE id = inpId;
    END;
    
    PROCEDURE MyDelete(inpId NUMBER)IS
    BEGIN
        DELETE FROM MyTable WHERE id = inpId;
    END;
        
    FUNCTION CalculateTotalCompensation(p_monthly_salary NUMBER, p_annual_bonus_percentage NUMBER)
    RETURN NUMBER IS
        v_annual_bonus_percentage NUMBER;
        v_total_compensation NUMBER;
        annual_bonus_percentage_exception EXCEPTION;
        monthly_salary_exception EXCEPTION;
    BEGIN
        -- проверка процента годовых премиальных
        IF p_annual_bonus_percentage <= 0 OR p_annual_bonus_percentage > 100 THEN
            RAISE annual_bonus_percentage_exception;
        END IF;
    
        -- проверка месячной зарплаты
            IF p_monthly_salary <= 0 
            THEN
                RAISE monthly_salary_exception;
            END IF;    
    
        -- преобразование процента к дробному виду
            v_annual_bonus_percentage := p_annual_bonus_percentage / 100;
    
        -- вычисление общего вознаграждения
            v_total_compensation := (1 + v_annual_bonus_percentage) * 12 * p_monthly_salary;
    
            RETURN v_total_compensation;
    EXCEPTION
        WHEN annual_bonus_percentage_exception THEN
            dbms_output.put_line('Некорректное значение процента годовых премиальных');
            RAISE annual_bonus_percentage_exception;
        WHEN monthly_salary_exception THEN
            dbms_output.put_line('Некорректное значение месячной зарплаты');
            RAISE monthly_salary_exception;
    END CalculateTotalCompensation;
BEGIN

    SELECT COUNT(*) INTO countvar FROM MyTable;
    IF (countvar != 0)
    THEN
        DBMS_OUTPUT.put_line('There is some elements in table');
        
        Analyze();
        GenerateInsert(212);
    ELSE
        FOR i IN 1..10 LOOP
            res := dbms_random.value(0, 40000);
            INSERT INTO MyTable(val) VALUES (res);
        END LOOP;
    END IF; 
END;