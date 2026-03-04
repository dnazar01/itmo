DROP TABLE IF EXISTS usr_wrk.mart_evt_all;

CREATE TABLE usr_wrk.mart_evt_all AS

/* ---------- 9 vitрин, одинаковая маска ---------- */
SELECT event_type::text,
       event_id::text,
       task_id::text,
       dttm::timestamp,
       first_task_id::text
FROM usr_wrk.mart_evt_status

UNION ALL
SELECT event_type::text, event_id::text, task_id::text, dttm, first_task_id::text
FROM usr_wrk.mart_evt_notes

UNION ALL
SELECT event_type::text, event_id::text, task_id::text, dttm, first_task_id::text
FROM usr_wrk.mart_evt_escalations

UNION ALL
SELECT event_type::text, event_id::text, task_id::text, dttm, first_task_id::text
FROM usr_wrk.mart_evt_consultations

UNION ALL
SELECT event_type::text, event_id::text, task_id::text, dttm, first_task_id::text
FROM usr_wrk.mart_evt_calls_back -- флаг _back

UNION ALL
SELECT event_type::text, event_id::text, task_id::text, dttm, first_task_id::text
FROM usr_wrk.mart_evt_chats

UNION ALL
SELECT event_type::text, event_id::text, task_id::text, dttm, first_task_id::text
FROM usr_wrk.mart_evt_csat

UNION ALL
SELECT event_type::text, event_id::text, task_id::text, dttm, first_task_id::text
FROM usr_wrk.mart_evt_deadline

UNION ALL
SELECT event_type::text, event_id::text, task_id::text, dttm, first_task_id::text
FROM usr_wrk.mart_evt_label;