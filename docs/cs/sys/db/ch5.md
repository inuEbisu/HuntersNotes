---
comment: true
---

# Ch 5. Advanced SQL

## Accessing SQL from a Programming Language

There are two primary ways to access SQL from a Programming Language:

- **API (Application Program Interface):** Using libraries like **ODBC (C, C++, ...)** or **JDBC (Java)** and ORMs like **JPA**.

- **Embedding SQL:** Directly embedding statements into the host language (e.g., **SQLJ**).

### JDBC (Java DataBase Connectivity)

A standard lifecycle:

- Connection
- Statement
- Execute
- Exception handling
- Close

??? example

    ```java
    import java.sql.*;

    public class DatabaseApp {
        public static void JDBCExample(String url, String user, String password) {
            Connection conn = null;
            try {
                // 1. Establish Connection
                conn = DriverManager.getConnection(url, user, password);

                // 2. Transaction Management: Disable Auto-Commit
                conn.setAutoCommit(false);

                // 3. Prepared Statement (Prevents SQL Injection)
                String sql = "INSERT INTO instructor (ID, name, dept_name, salary) VALUES (?, ?, ?, ?)";
                PreparedStatement pStmt = conn.prepareStatement(sql);
                pStmt.setString(1, "88877");
                pStmt.setString(2, "Einstein");
                pStmt.setString(3, "Physics");
                pStmt.setDouble(4, 95000);
                pStmt.executeUpdate();

                // 4. Executing Query & ResultSet
                Statement stmt = conn.createStatement();
                ResultSet rset = stmt.executeQuery("SELECT dept_name, salary FROM instructor");

                while (rset.next()) {
                    // Access by column name or index (starts at 1)
                    System.out.println(rset.getString("dept_name") + " " + rset.getFloat(2));
                }

                // 5. Metadata: Extracting Database Structure
                ResultSetMetaData rsmd = rset.getMetaData();
                int columnCount = rsmd.getColumnCount();
                System.out.println("Column count: " + columnCount);
                for (int i = 1; i <= columnCount; i++) {
                    System.out.println("Column " + i + ": " + rsmd.getColumnName(i));
                }

                // 6. Commit Transaction
                conn.commit();

            } catch (SQLException e) {
                // 7. Exception Handling & Rollback
                System.err.println("SQL Error: " + e.getMessage());
                try { if (conn != null) conn.rollback(); } catch (SQLException ex) { ex.printStackTrace(); }
            } finally {
                // 8. Resource Cleanup
                try { if (conn != null) conn.close(); } catch (SQLException e) { e.printStackTrace(); }
            }
        }
    }
    ```

### ODBC (Open DataBase Connectivity)

??? example

    ```c
    #include <sql.h>
    #include <sqlext.h>
    #include <stdio.h>

    int ODBCExample() {
        RETCODE error;
        HENV env;   // Environment handle
        HDBC conn;  // Connection handle
        HSTMT stmt; // Statement handle

        // 1. Initialization
        SQLAllocEnv(&env);
        SQLAllocConnect(env, &conn);

        // 2. Connection
        error = SQLConnect(conn, "univdb", SQL_NTS, "admin", SQL_NTS, "passwd", SQL_NTS);
        if (error != SQL_SUCCESS && error != SQL_SUCCESS_WITH_INFO) return -1;

        // 3. Transaction: Turn off Autocommit
        SQLSetConnectOption(conn, SQL_AUTOCOMMIT, SQL_AUTOCOMMIT_OFF);

        // 4. Prepared Statement
        SQLAllocStmt(conn, &stmt);
        char* sql_insert = "INSERT INTO instructor VALUES (?, ?, ?, ?)";
        SQLPrepare(stmt, (SQLCHAR*)sql_insert, SQL_NTS);

        // Bind parameters (example for one ID column)
        char id[5] = "1234";
        SQLBindParameter(stmt, 1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_CHAR, 5, 0, id, 0, NULL);
        SQLExecute(stmt);

        // 5. Executing Query & Metadata
        char* sql_query = "SELECT dept_name, salary FROM instructor";
        SQLExecDirect(stmt, (SQLCHAR*)sql_query, SQL_NTS);

        SQLSMALLINT cols;
        SQLNumResultCols(stmt, &cols); // Metadata: get number of columns
        printf("Result set has %d columns\n", cols);

        // 6. Binding Columns & Fetching Data
        char deptname[80];
        float salary;
        SQLLEN len1, len2;
        SQLBindCol(stmt, 1, SQL_C_CHAR, deptname, 80, &len1);
        SQLBindCol(stmt, 2, SQL_C_FLOAT, &salary, 0, &len2);

        while (SQLFetch(stmt) == SQL_SUCCESS) {
            printf("Dept: %s, Salary: %f\n", deptname, salary);
        }

        // 7. Transaction: Commit or Rollback
        SQLTransact(env, conn, SQL_COMMIT);

        // 8. Cleanup
        SQLFreeStmt(stmt, SQL_DROP);
        SQLDisconnect(conn);
        SQLFreeConnect(conn);
        SQLFreeEnv(env);

        return 0;
    }
    ```

## Procedural SQL

Allows business logic to be stored and executed directly within the database. For speed!

Functions return a value, while procedures are called to perform actions and can return multiple values via parameters.

### Functions

```sql
-- CREATE FUNCTION ...(...)
-- RETURNS ...
-- BEGIN
-- ...; RETURN ...;
-- END;

CREATE FUNCTION dept_count(dept_name VARCHAR(20))
RETURNS INTEGER
BEGIN
    DECLARE d_count INTEGER;
    SELECT count(*) INTO d_count FROM instructor
    WHERE instructor.dept_name = dept_name;
    RETURN d_count;
END;

SELECT dept_name, budget
FROM department
WHERE dept_count(dept_name) > 12;
```

Table functions (parameterized materialized views):

```sql
-- RETURNS TABLE( , , , )
-- RETURN TABLE(...)

CREATE FUNCTION instructor_of(dept_name VARCHAR(20))
    RETURNS TABLE(
        ID VARCHAR(5),
        name VARCHAR(20),
        dept_name VARCHAR(20),
        salary NUMERIC(8, 2)
    )
    RETURN TABLE(
        SELECT ID, name, dept_name, salary
        FROM instructor
        WHERE instructor.dept_name = instructor_of.dept_name
    );
```

### Procedures

```sql
-- CREATE PROCEDURE ...(IN ..., OUT ...)
-- BEGIN
-- ... INTO ...
-- END
CREATE PROCEDURE dept_count_proc(IN dept_name VARCHAR(20), OUT d_count INTEGER)
BEGIN
    SELECT count(*) INTO d_count FROM instructor
    WHERE instructor.dept_name = dept_name;
END;

DECLARE d_count INTEGER;
CALL dept_count_proc('Physics', d_count);
```

### Procedural Constructs

```sql
DECLARE n INTEGER DEFAULT 0;
-- WHILE ... DO ... END WHILE
WHILE n < 10 DO
    SET n = n + 1;
END WHILE;

-- REPEAT ... UNTIL ... END REPEAT
REPEAT
    SET n = n - 1
UNTIL n = 0
END REPEAT

-- FOR ... AS ...
-- DO ...
-- END FOR
DECLARE n INTEGER DEFAULT 0;
FOR r AS -- for each row
    SELECT budget FROM department
    WHERE dept_name = 'Music'
DO
    SET n = n - r.budget
END FOR
```

### Triggers

Triggers are actions executed automatically by the system as a side effect of a modification (Insert, Update, Delete). They follow the **ECA Rule (Event, Condition, Action)**.

### Recursive Queries

Used to solve transitive closure problems.

```sql
-- WITH RECURSIVE ...(...) AS (...)

WITH RECURSIVE rec_prereq(course_id, prereq_id) AS (
    SELECT course_id, prereq_id FROM prereq
  UNION
    SELECT rec_prereq.course_id, prereq.prereq_id
    FROM rec_prereq, prereq
    WHERE rec_prereq.prereq_id = prereq.course_id
)
SELECT * FROM rec_prereq;
```
