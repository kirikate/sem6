--������� 1
/*CREATE TABLE Students(
    id NUMBER NOT NULL,
    name VARCHAR2(30) NOT NULL,
    group_id NUMBER NOT NULL)

CREATE TABLE Groupes(
    id NUMBER NOT NULL,
    name VARCHAR2(40) NOT NULL,
    c_val NUMBER NOT NULL) */

--������� 2
/*CREATE SEQUENCE student_id_sequence
START WITH 1
INCREMENT BY 1;*/

CREATE OR REPLACE TRIGGER generate_student_id
BEFORE INSERT ON Students                                                                                                                                                                                  
FOR EACH ROW
BEGIN
    IF :new.id IS NULL THEN
        :new.id := student_id_sequence.nextval;
    END IF;
END;
/
/*CREATE SEQUENCE group_id_sequence
START WITH 1
INCREMENT BY 1;*/
/
CREATE OR REPLACE TRIGGER generate_group_id
BEFORE INSERT ON Groupes
FOR EACH ROW
BEGIN
    IF :new.id IS NULL THEN
        :new.id := group_id_sequence.nextval;
    END IF;
END;
/
--------------------------
/*CREATE TABLE Cascad (
    id NUMBER NOT NULL,
    is_cascad NUMBER NOT NULL
)
*/

INSERT INTO cascad VALUES (1, 0);
/

--������� 3
CREATE OR REPLACE TRIGGER fk_group_delete_cascad
 AFTER DELETE ON Groups
 FOR EACH ROW
BEGIN
    UPDATE cascad SET is_cascad = 1 WHERE id = 1;
    DELETE FROM Students WHERE group_id = :OLD.id;
    UPDATE cascad SET is_cascad = 0 WHERE id = 1;
END;
/


--������� 4
/*CREATE TABLE student_journal (
    id NUMBER PRIMARY KEY,
    operation VARCHAR2(10),
    op_time TIMESTAMP,
    s_id NUMBER,
    s_name VARCHAR2(30),
    s_group_id NUMBER,
    n_s_id NUMBER,
    n_s_name VARCHAR2(30),
    n_s_group_id NUMBER
);*/
/*

CREATE SEQUENCE stud_journal_id_seq
START WITH 1
INCREMENT BY 1;
*/

CREATE OR REPLACE TRIGGER students_journal
 AFTER INSERT OR UPDATE OR DELETE ON Students
 FOR EACH ROW
BEGIN
    IF INSERTING THEN
        INSERT INTO student_journal VALUES (stud_journal_id_seq.nextval, 'INSERT', CURRENT_TIMESTAMP, :NEW.id, :NEW.name, :NEW.group_id, NULL, NULL, NULL);
    END IF;

    IF UPDATING THEN
        INSERT INTO student_journal VALUES (stud_journal_id_seq.nextval, 'UPDATE', CURRENT_TIMESTAMP, :OLD.id, :OLD.name, :OLD.group_id, :NEW.id, :NEW.name, :NEW.group_id);
    END IF;
        
    IF DELETING THEN
        INSERT INTO student_journal VALUES (stud_journal_id_seq.nextval, 'DELETE', CURRENT_TIMESTAMP, :OLD.id, :OLD.name, :OLD.group_id, NULL, NULL, NULL);
    END IF;
END;

/

--������� 5
CREATE OR REPLACE PROCEDURE rollback_students(r_time TIMESTAMP) IS
BEGIN
    FOR action IN (SELECT * FROM student_journal WHERE r_time < op_time ORDER BY id DESC)
    LOOP
        CASE action.operation
            WHEN 'INSERT' THEN
                DELETE Students WHERE id = action.s_id;

            WHEN 'UPDATE' THEN
                UPDATE Students
                SET id = action.s_id,
                    name = action.s_name,
                    group_id = action.s_group_id
                WHERE id = action.n_s_id;

            WHEN 'DELETE' THEN
                INSERT INTO Students VALUES (action.s_id, action.s_name, action.s_group_id);
        END CASE;
    END LOOP;
END;
/

CREATE OR REPLACE PROCEDURE rollback_students_by_offset(offset NUMBER) IS
BEGIN
    rollback_students(TO_TIMESTAMP(CURRENT_TIMESTAMP - INTERVAL '1'MINUTE * offset ));
END;
/


--������� 6
CREATE OR REPLACE TRIGGER c_val_trigger
AFTER INSERT OR UPDATE OR DELETE ON Students
FOR EACH ROW
DECLARE
    v_is_cascade NUMBER;
BEGIN 
    IF UPDATING THEN
        UPDATE Groupes
        SET c_val = c_val + 1
        WHERE id = :NEW.group_id;

        UPDATE Groupes
        SET c_val = c_val - 1
        WHERE id = :OLD.group_id;
    ELSIF INSERTING THEN
        UPDATE Groupes
        SET c_val = c_val + 1
        WHERE id = :NEW.group_id;
    ELSIF DELETING THEN
        SELECT is_cascad INTO v_is_cascade FROM cascad WHERE id = 1;

        IF v_is_cascade = 1 THEN
            RETURN;
        ELSE
            UPDATE Groupes
            SET c_val = c_val - 1
            WHERE id = :OLD.group_id;
        END IF;
    END IF;
END;
/

DELETE FROM Students;
DELETE FROM Groupes;
DELETE FROM student_journal;


INSERT INTO Groupes(id, name, c_val) VALUES (1, '153502', 0);
INSERT INTO Groupes(id, name, c_val) VALUES (2, '153503', 0);
INSERT INTO Groupes(name, c_val) VALUES ( '153504', 0);
SELECT * FROM Groupes;

INSERT INTO Students(id, name, group_id) VALUES (1, 'Anton', 1);
INSERT INTO Students(name, group_id) VALUES ('Boris', 1);
INSERT INTO Students(name, group_id) VALUES ('Vlad', 2);
SELECT * FROM Students;

--�������� ������������� ������� ������ � ��� �� ����
INSERT INTO Groupes(id, name, c_val) VALUES (1, '153505', 0);

--�������� ������������� ������� ������ � ��� �� ������
INSERT INTO Groupes(name, c_val) VALUES ('153502', 0);


--�������� ������������ id ��������
INSERT INTO Students(id, name, group_id) VALUES (1, 'Vassya', 1);

--�������� ���������� ��������
delete from groupes where name = '153503';
SELECT * FROM Students;

--�������� ��������������
--SELECT * FROM stud_journal

--�������� �������� �� ��������� �����
--call roll_back_students(TO_TIMESTAMP ('23.02.24 14:10:10.123000', 'DD.MM.RRRR HH24:MI:SS.FF'))

--�������� �������� �� ��������
--call roll_back_students_by_offset(��� ������);

DELETE FROM Students;
DELETE FROM Groupes;
DELETE FROM student_journal;