drop TABLE if EXISTS usr_wrk.mart_evt_notes;

      create table usr_wrk.mart_evt_notes as (
            SELECT DISTINCT
             event_type, event_id, task_id, dttm,
             COALESCE(first_task_id, task_id) AS first_task_id,
             note_txt
            FROM   (
                  -- Заметки
                  SELECT
                        'note'  AS event_type,
                        notes.crm_task_note_rk::text               AS event_id,
                        srs.task_sr_id::text                     AS task_id,
                        notes.create_dttm                     AS dttm,
                        first_task_id::text                  AS first_task_id,
                        notes.note_txt
                  FROM   usr_cspa.dko_tasks_srs_overview srs
                  left JOIN prod_v_dds.crm_task_note            notes
                        ON notes.crm_task_rk = srs.task_sr_rk
                        and srs.client_non_client = 'Клиентский'
                        and srs.party_rk is not null
                        and notes.visibility_code = 'CLIENT'
                  WHERE  notes.create_dttm >= DATE '2025-04-01' and notes.create_dttm < DATE '2025-07-01'
            ) t1
      )
     