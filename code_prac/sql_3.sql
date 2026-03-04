DROP TABLE IF EXISTS valid_task_numbers;
      CREATE TABLE valid_task_numbers AS

      WITH overview_norm AS (
          SELECT DISTINCT
                 task_sr_id AS task_id
          FROM   usr_cspa.dko_tasks_srs_overview
          WHERE  napravlenie_last = 'Бэк-офис'
      ),

      valid_tasks AS (
          SELECT fl.task_id
          FROM (
              SELECT
                  task_id,
                  FIRST_VALUE(event_type) OVER w_last  AS last_event_type,
                  FIRST_VALUE(event_type) OVER w_first AS first_event_type
              FROM usr_wrk.mart_evt_status
              WINDOW w_last  AS (PARTITION BY task_id ORDER BY dttm DESC),
                     w_first AS (PARTITION BY task_id ORDER BY dttm ASC)
          ) fl
          JOIN overview_norm bo USING (task_id)
          WHERE fl.last_event_type  = 'task_closed'
            AND fl.first_event_type = 'task_opened'
      ),

      deadline_first AS (
          SELECT DISTINCT task_id
          FROM (
              SELECT
                  task_id,
                  FIRST_VALUE(event_type) OVER (PARTITION BY task_id ORDER BY dttm ASC) AS first_event
              FROM usr_wrk.mart_evt_all_enriched
          ) t
          WHERE first_event = 'deadline_set'
      ),

      eligible_tasks AS (
          SELECT v.task_id
          FROM   valid_tasks v
          LEFT   JOIN deadline_first d USING (task_id)
          WHERE  d.task_id IS NULL
      ),

      scored AS (
          SELECT
              me.*,
              LN(1 + escalation_cnt
                    + deadline_shift_cnt
                    + outgoing_call_cnt
                    + outgoing_note_cnt
                    + frontline_msg_cnt
                    + is_repeat
                    + resolution_days) AS log_effort
          FROM usr_wrk.mart_task_efforts me
          JOIN eligible_tasks et USING (task_id)
          WHERE crm_task_no IS NOT NULL
            AND (outgoing_call_cnt + outgoing_note_cnt) > 0
            AND (escalation_cnt + deadline_shift_cnt + outgoing_call_cnt
                 + outgoing_note_cnt + frontline_msg_cnt + is_repeat + resolution_days) > 0
      ),

      quartiled AS (
          SELECT
              scored.*,
              NTILE(4) OVER (ORDER BY log_effort) AS effort_q
          FROM scored
      ),

      deduplicated AS (
          SELECT *
          FROM (
              SELECT *,
                     ROW_NUMBER() OVER (PARTITION BY task_id ORDER BY log_effort DESC) AS task_rn
              FROM quartiled
          ) t
          WHERE task_rn = 1
      ),
         -- Все задачи со звонками
      outgoing_calls AS (
          SELECT DISTINCT cb.task_id
          FROM usr_wrk.mart_evt_calls_back cb
          WHERE cb.event_type = 'outgoing_call'
      ),

      -- Звонковые задачи с усилиями
      calls_with_data AS (
          SELECT
              me.task_id,
              me.crm_task_no,
              me.escalation_cnt,
              me.deadline_shift_cnt,
              me.outgoing_call_cnt,
              me.outgoing_note_cnt,
              me.frontline_msg_cnt,
              me.is_repeat,
              me.resolution_days,
              LN(1 + me.escalation_cnt
                     + me.deadline_shift_cnt
                     + me.outgoing_call_cnt
                     + me.outgoing_note_cnt
                     + me.frontline_msg_cnt
                     + me.is_repeat
                     + me.resolution_days) AS log_effort,
              NULL::int AS effort_q
          FROM usr_wrk.mart_task_efforts me
          JOIN outgoing_calls cb USING (task_id)
      ),

      -- Считаем сколько тасков со звонками
      calls_count AS (
          SELECT COUNT(*) AS cnt FROM calls_with_data
      ),

      -- Основная выборка без звонков, с ранжированием по квартилям
      ranked AS (
          SELECT *,
                 ROW_NUMBER() OVER (PARTITION BY effort_q ORDER BY RANDOM()) AS rn
          FROM deduplicated
          WHERE task_id NOT IN (SELECT task_id FROM calls_with_data)
      ),

      -- Финальные таски по квартилям (равномерно по оставшимся)
      main_sample AS (
          SELECT r.*
          FROM ranked r
          JOIN calls_count c ON TRUE
          WHERE r.rn <= (5000 - c.cnt) / 4
      ),

      -- Объединяем
      final_union AS (
          SELECT
              task_id,
              crm_task_no,
              escalation_cnt,
              deadline_shift_cnt,
              outgoing_call_cnt,
              outgoing_note_cnt,
              frontline_msg_cnt,
              is_repeat,
              resolution_days,
              log_effort,
              effort_q
          FROM main_sample

          UNION ALL

          SELECT
              task_id,
              crm_task_no,
              escalation_cnt,
              deadline_shift_cnt,
              outgoing_call_cnt,
              outgoing_note_cnt,
              frontline_msg_cnt,
              is_repeat,
              resolution_days,
              log_effort,
              effort_q
          FROM calls_with_data
      )

      SELECT *
      FROM final_union;