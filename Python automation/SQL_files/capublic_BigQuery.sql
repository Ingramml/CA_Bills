-- ----------------------------------------------------------------------------+
-- capublic.sql - Create all the capublic tables in MySQL database.
--
--  ---When---  ---Who---  ------------------What---------------------
--  2009-02-18  Rudy-H.    Created script to add tables.
--  2010-04-05  Rudy-H.    Added field DAYS_31ST_IN_PRINT to table
--                         BILL_TBL.
--  2010-05-18  Rudy-H.    Added field MEMBER_ORDER to table
--                         BILL_DETAIL_VOTE_TBL.
--  2011-03-18  Rudy-H.    Added more fields, indexes and changed fields.
--                         See changes_diff.txt file for actual changes.
--  2012-05-09  Rudy-H.    Added new table veto_message_tbl.
--
-- ----------------------------------------------------------------------------+



-- -------------------------------------
-- Database
-- -------------------------------------
CREATE DATABASE  capublic
  CHARACTER SET utf8 COLLATE  utf8_general_ci;




-- -------------------------------------
-- Tables
-- -------------------------------------
DROP TABLE IF EXISTS capublic.bill_analysis_tbl;
CREATE TABLE capublic.bill_analysis_tbl     (
  analysis_id                 NUMERIC(22, 0)          NOT NULL,
  bill_id                     STRING(20)       NOT NULL,
  house                       STRING(1)        NULL,
  analysis_type               STRING(100)      NULL,
  committee_code              STRING(6)        NULL,
  committee_name              STRING(200)      NULL,
  amendment_author            STRING(100)      NULL,
  analysis_date               DATETIME                NULL,
  amendment_date              DATETIME                NULL,
  page_num                    NUMERIC(22, 0)          NULL,
  source_doc                  BYTES                NULL,
  released_floor              STRING(1)        NULL,
  active_flg                  STRING(1)        NULL DEFAULT 'Y',
  trans_uid                   STRING(20)       NULL,
  trans_update                DATETIME                NULL,
  PRIMARY KEY (analysis_id),
  INDEX bill_analysis_bill_id_idx  (bill_id(20))
)

;

DROP TABLE IF EXISTS capublic.bill_detail_vote_tbl;
CREATE TABLE capublic.bill_detail_vote_tbl  (
  bill_id                     STRING(20)       NOT NULL,
  location_code               STRING(6)        NOT NULL,
  legislator_name             STRING(50)       NOT NULL,
  vote_date_time              DATETIME                NOT NULL,
  vote_date_seq               INT64(4)                  NOT NULL,
  vote_code                   STRING(5)        NULL,
  motion_id                   INT64(8)                  NOT NULL,
  trans_uid                   STRING(30)       NULL,
  trans_update                DATETIME                NULL,
  member_order                INT64(4)                  NULL,
  session_date                DATETIME                NULL,
  speaker                     STRING(1)        NULL,
  INDEX author_votecode_idx   (legislator_name(50), vote_code(5)),
  INDEX bill_detail_vote_id_idx       (bill_id(20)),
  INDEX check_dup_detail_vote_idx     (bill_id(20), vote_date_time, location_code(6), motion_id, legislator_name(50), vote_date_seq)
)

;

DROP TABLE IF EXISTS capublic.bill_history_tbl;
CREATE TABLE capublic.bill_history_tbl      (
  bill_id                     STRING(20)       NULL,
  bill_history_id             NUMERIC(20, 0)          NULL,
  action_date                 DATETIME                NULL,
  action                      STRING(2000)     NULL,
  trans_uid                   STRING(20)       NULL,
  trans_update_dt             DATETIME                NULL,
  action_sequence             INT64(4)                  NULL,
  action_code                 STRING(5)        NULL,
  action_status               STRING(60)       NULL,
  primary_location            STRING(60)       NULL,
  secondary_location          STRING(60)       NULL,
  ternary_location            STRING(60)       NULL,
  end_status                  STRING(60)       NULL,
  INDEX bill_history_id_idx   (bill_id(20))
)

;

DROP TABLE IF EXISTS capublic.bill_motion_tbl;
CREATE TABLE capublic.bill_motion_tbl       (
  motion_id                   NUMERIC(20, 0)          NOT NULL,
  motion_text                 STRING(250)      NULL,
  trans_uid                   STRING(30)       NULL,
  trans_update                DATETIME                NULL,
  PRIMARY KEY (motion_id)
)

;

DROP TABLE IF EXISTS capublic.bill_summary_vote_tbl;
CREATE TABLE capublic.bill_summary_vote_tbl (
  bill_id                     STRING(20)       NOT NULL,
  location_code               STRING(6)        NOT NULL,
  vote_date_time              DATETIME                NOT NULL,
  vote_date_seq               INT64(4)                  NOT NULL,
  motion_id                   INT64(8)                  NOT NULL,
  ayes                        INT64(3)                  NULL,
  noes                        INT64(3)                  NULL,
  abstain                     INT64(3)                  NULL,
  vote_result                 STRING(6)        NULL,
  trans_uid                   STRING(30)       NULL,
  trans_update                DATETIME                NULL,
  file_item_num               STRING(10)       NULL,
  file_location               STRING(50)       NULL,
  display_lines               STRING(2000)     NULL,
  session_date                DATETIME                NULL,
  INDEX bill_summary_vote_id_idx      (bill_id(20)),
  INDEX bill_summary_vote_mo_idx      (motion_id),
  INDEX check_dup_summary_vote_idx    (bill_id(20), motion_id, vote_date_time, vote_date_seq, location_code(6))
)

;

DROP TABLE IF EXISTS capublic.bill_tbl;
CREATE TABLE capublic.bill_tbl      (
  bill_id                     STRING(19)       NOT NULL,
  session_year                STRING(8)        NOT NULL,
  session_num                 STRING(2)        NOT NULL,
  measure_type                STRING(4)        NOT NULL,
  measure_num                 INT64(5)                  NOT NULL,
  measure_state               STRING(40)       NOT NULL,
  chapter_year                STRING(4)        NULL,
  chapter_type                STRING(10)       NULL,
  chapter_session_num         STRING(2)        NULL,
  chapter_num                 STRING(10)       NULL,
  latest_bill_version_id      STRING(30)       NULL,
  active_flg                  STRING(1)        NULL DEFAULT 'Y',
  trans_uid                   STRING(30)       NULL,
  trans_update                DATETIME                NULL,
  current_location            STRING(200)      NULL,
  current_secondary_loc       STRING(60)       NULL,
  current_house               STRING(60)       NULL,
  current_status              STRING(60)       NULL,
  days_31st_in_print          DATETIME                NULL,
  PRIMARY KEY (bill_id),
  INDEX bill_tbl_chapter_year_idx     (chapter_year(4)),
  INDEX bill_tbl_measure_num_idx      (measure_num),
  INDEX bill_tbl_measure_type_idx     (measure_type(4)),
  INDEX bill_tbl_session_idx          (session_year(8)),
  INDEX bill_tbl__ltst_bill_ver_idx   (latest_bill_version_id(30))
)

;

DROP TABLE IF EXISTS capublic.bill_version_authors_tbl;
CREATE TABLE capublic.bill_version_authors_tbl      (
  bill_version_id             STRING(30)       NOT NULL,
  type                        STRING(15)       NOT NULL,
  house                       STRING(100)      NULL,
  name                        STRING(100)      NULL,
  contribution                STRING(100)      NULL,
  committee_members           STRING(2000)     NULL,
  active_flg                  STRING(1)        NULL DEFAULT 'Y',
  trans_uid                   STRING(30)       NULL,
  trans_update                DATETIME                NULL,
  primary_author_flg          STRING(1)        NULL DEFAULT 'N',
  INDEX bill_version_auth_tbl_id_idx  (bill_version_id(30)),
  Index bill_version_auth_tbl_name_idx (name)
)

;

DROP TABLE IF EXISTS capublic.bill_version_tbl;
CREATE TABLE capublic.bill_version_tbl      (
  bill_version_id             STRING(30)       NOT NULL,
  bill_id                     STRING(19)       NOT NULL,
  version_num                 INT64(2)                  NOT NULL,
  bill_version_action_date    DATETIME                NOT NULL,
  bill_version_action         STRING(100)      NULL,
  request_num                 STRING(10)       NULL,
  subject                     STRING(1000)     NULL,
  vote_required               STRING(100)      NULL,
  appropriation               STRING(3)        NULL,
  fiscal_committee            STRING(3)        NULL,
  local_program               STRING(3)        NULL,
  substantive_changes         STRING(3)        NULL,
  urgency                     STRING(3)        NULL,
  taxlevy                     STRING(3)        NULL,
  bill_xml                    STRING          NULL,
  active_flg                  STRING(1)        NULL DEFAULT 'Y',
  trans_uid                   STRING(30)       NULL,
  trans_update                DATETIME                NULL,
  PRIMARY KEY (bill_version_id),
  Index bill_version_tbl_bill_id_idx (bill_id(19)),
  Index bill_version_tbl_version_idx (version_num)
)

;

DROP TABLE IF EXISTS capublic.codes_tbl;
CREATE TABLE capublic.codes_tbl     (
  code                        STRING(5)        NULL,
  title                       STRING(2000)     NULL
)

;

DROP TABLE IF EXISTS capublic.committee_hearing_tbl;
CREATE TABLE capublic.committee_hearing_tbl (
  bill_id                     STRING(20)       NULL,
  committee_type              STRING(2)        NULL,
  committee_nr                INT64(5)                  NULL,
  hearing_date                DATETIME                NULL,
  location_code               STRING(6)        NULL,
  trans_uid                   STRING(30)       NULL,
  trans_update_date           DATETIME                NULL,
  Index committee_hear_bill_id_idx (bill_id(20))
)

;

DROP TABLE IF EXISTS capublic.daily_file_tbl;
CREATE TABLE capublic.daily_file_tbl        (
  bill_id                     STRING(20)       NULL,
  location_code               STRING(6)        NULL,
  consent_calendar_code       INT64(2)                  NULL,
  file_location               STRING(6)        NULL,
  publication_date            DATETIME                NULL,
  floor_manager               STRING(100)      NULL,
  trans_uid                   STRING(20)       NULL,
  trans_update_date           DATETIME                NULL,
  session_num                 STRING(2)        NULL,
  status                      STRING(200)      NULL,
  Index daily_file_pub_date_idx (publication_date),
  Index daily_file_tbl_bill_id_idx (bill_id(20))
)

;

DROP TABLE IF EXISTS capublic.law_section_tbl;
CREATE TABLE capublic.law_section_tbl       (
  id                          STRING(100)      NULL,
  law_code                    STRING(5)        NULL,
  section_num                 STRING(30)       NULL,
  op_statues                  STRING(10)       NULL,
  op_chapter                  STRING(10)       NULL,
  op_section                  STRING(20)       NULL,
  effective_date              DATETIME                NULL,
  law_section_version_id      STRING(100)      NULL,
  division                    STRING(100)      NULL,
  title                       STRING(100)      NULL,
  part                        STRING(100)      NULL,
  chapter                     STRING(100)      NULL,
  article                     STRING(100)      NULL,
  history                     STRING(1000)     NULL,
  content_xml                 STRING          NULL,
  active_flg                  STRING(1)        NULL DEFAULT 'Y',
  trans_uid                   STRING(30)       NULL,
  trans_update                DATETIME                NULL,
  INDEX law_section_tbl_pk   (id(100)),
  Index law_section_code_idx (law_code(5)),
  Index law_section_id_idx (law_section_version_id(100)),
  Index law_section_sect_idx (section_num(30))
)

;

DROP TABLE IF EXISTS capublic.law_toc_sections_tbl;
CREATE TABLE capublic.law_toc_sections_tbl  (
  id                          STRING(100)      NULL,
  law_code                    STRING(5)        NULL,
  node_treepath               STRING(100)      NULL,
  section_num                 STRING(30)       NULL,
  section_order               NUMERIC(22, 0)          NULL,
  title                       STRING(400)      NULL,
  op_statues                  STRING(10)       NULL,
  op_chapter                  STRING(10)       NULL,
  op_section                  STRING(20)       NULL,
  trans_uid                   STRING(30)       NULL,
  trans_update                DATETIME                NULL,
  law_section_version_id      STRING(100)      NULL,
  seq_num                     NUMERIC(22, 0)          NULL,
  Index law_toc_sections_node_idx (law_code(5), node_treepath(100))
)

;

DROP TABLE IF EXISTS capublic.law_toc_tbl;
CREATE TABLE capublic.law_toc_tbl   (
  law_code                    STRING(5)        NULL,
  division                    STRING(100)      NULL,
  title                       STRING(100)      NULL,
  part                        STRING(100)      NULL,
  chapter                     STRING(100)      NULL,
  article                     STRING(100)      NULL,
  heading                     STRING(2000)     NULL,
  active_flg                  STRING(1)        NULL DEFAULT 'Y',
  trans_uid                   STRING(30)       NULL,
  trans_update                DATETIME                NULL,
  node_sequence               NUMERIC(22, 0)          NULL,
  node_level                  NUMERIC(22, 0)          NULL,
  node_position               NUMERIC(22, 0)          NULL,
  node_treepath               STRING(100)      NULL,
  contains_law_sections       STRING(1)        NULL,
  history_note                STRING(350)      NULL,
  op_statues                  STRING(10)       NULL,
  op_chapter                  STRING(10)       NULL,
  op_section                  STRING(20)       NULL,
  Index law_toc_article_idx (article(100)),
  Index law_toc_chapter_idx (chapter(100)),
  Index law_toc_code_idx (law_code(5)),
  Index law_toc_division_idx (division(100)),
  Index law_toc_part_idx (part(100)),
  Index law_toc_title_idx (title(100))
)

;

DROP TABLE IF EXISTS capublic.legislator_tbl;
CREATE TABLE capublic.legislator_tbl        (
  district                    STRING(5)        NOT NULL,
  session_year                STRING(8)        NULL,
  legislator_name             STRING(30)       NULL,
  house_type                  STRING(1)        NULL,
  author_name                 STRING(200)      NULL,
  first_name                  STRING(30)       NULL,
  last_name                   STRING(30)       NULL,
  middle_initial              STRING(1)        NULL,
  name_suffix                 STRING(12)       NULL,
  name_title                  STRING(34)       NULL,
  web_name_title              STRING(34)       NULL,
  party                       STRING(4)        NULL,
  active_flg                  STRING(1)        NOT NULL DEFAULT 'Y',
  trans_uid                   STRING(30)       NULL,
  trans_update                DATETIME                NULL,
  active_legislator           STRING(1)        NULL DEFAULT 'Y'
)

;

DROP TABLE IF EXISTS capublic.location_code_tbl;
CREATE TABLE capublic.location_code_tbl     (
  session_year                STRING(8)        NULL,
  location_code               STRING(6)        NOT NULL,
  location_type               STRING(1)        NOT NULL,
  consent_calendar_code       STRING(2)        NULL,
  description                 STRING(60)       NULL,
  long_description            STRING(200)      NULL,
  active_flg                  STRING(1)        NULL DEFAULT 'Y',
  trans_uid                   STRING(30)       NULL,
  trans_update                DATETIME                NULL,
  inactive_file_flg           STRING(1)        NULL,
  INDEX location_code_tbl_pk1       (location_code(6)),
  Index localtion_code_session_idx1 (session_year(8))
)

;

DROP TABLE IF EXISTS capublic.veto_message_tbl;
CREATE TABLE capublic.veto_message_tbl (
  bill_id                     varchar(20)       NULL,
  veto_date                   datetime                NULL,
  message                     longtext          NULL,
  trans_uid                   varchar(20)       NULL,
  trans_update                datetime                NULL
)

;

DROP TABLE IF EXISTS capublic.committee_agenda_tbl;
CREATE TABLE capublic.committee_agenda_tbl (
  committee_code       varchar(200)      NULL,
  committee_desc       varchar(1000)     NULL,
  agenda_date          datetime                NULL,
  agenda_time          varchar(200)      NULL,
  line1                varchar(500)      NULL,
  line2                varchar(500)      NULL,
  line3                varchar(500)      NULL,
  building_type        varchar(200)      NULL,
  room_num             varchar(100)      NULL
)

;




-- --------------------------  E N D   O F  C O D E  --------------------------+
