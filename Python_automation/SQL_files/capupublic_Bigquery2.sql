-- ----------------------------------------------------------------------------+
-- capublic_BigQuery.sql - Create all the capublic tables in BigQuery dataset.
-- This script is rewritten for Google BigQuery SQL compatibility.
-- ----------------------------------------------------------------------------+

-- NOTE: You must create the BigQuery dataset 'capublic' before running this script.
-- Example: bq mk capublic

-- -------------------------------------
-- Tables
-- -------------------------------------

DROP TABLE IF EXISTS `capublic.bill_analysis_tbl`;
CREATE TABLE `capublic.bill_analysis_tbl` (
  analysis_id NUMERIC NOT NULL,
  bill_id STRING NOT NULL,
  house STRING,
  analysis_type STRING,
  committee_code STRING,
  committee_name STRING,
  amendment_author STRING,
  analysis_date DATETIME,
  amendment_date DATETIME,
  page_num NUMERIC,
  source_doc BYTES,
  released_floor STRING,
  active_flg STRING,
  trans_uid STRING,
  trans_update DATETIME
);

DROP TABLE IF EXISTS `capublic.bill_detail_vote_tbl`;
CREATE TABLE `capublic.bill_detail_vote_tbl` (
  bill_id STRING NOT NULL,
  location_code STRING NOT NULL,
  legislator_name STRING NOT NULL,
  vote_date_time DATETIME NOT NULL,
  vote_date_seq INT64 NOT NULL,
  vote_code STRING,
  motion_id INT64 NOT NULL,
  trans_uid STRING,
  trans_update DATETIME,
  member_order INT64,
  session_date DATETIME,
  speaker STRING
);

DROP TABLE IF EXISTS `capublic.bill_history_tbl`;
CREATE TABLE `capublic.bill_history_tbl` (
  bill_id STRING,
  bill_history_id NUMERIC,
  action_date DATETIME,
  action STRING,
  trans_uid STRING,
  trans_update_dt DATETIME,
  action_sequence INT64,
  action_code STRING,
  action_status STRING,
  primary_location STRING,
  secondary_location STRING,
  ternary_location STRING,
  end_status STRING
);

DROP TABLE IF EXISTS `capublic.bill_motion_tbl`;
CREATE TABLE `capublic.bill_motion_tbl` (
  motion_id NUMERIC NOT NULL,
  motion_text STRING,
  trans_uid STRING,
  trans_update DATETIME
);

DROP TABLE IF EXISTS `capublic.bill_summary_vote_tbl`;
CREATE TABLE `capublic.bill_summary_vote_tbl` (
  bill_id STRING NOT NULL,
  location_code STRING NOT NULL,
  vote_date_time DATETIME NOT NULL,
  vote_date_seq INT64 NOT NULL,
  motion_id INT64 NOT NULL,
  ayes INT64,
  noes INT64,
  abstain INT64,
  vote_result STRING,
  trans_uid STRING,
  trans_update DATETIME,
  file_item_num STRING,
  file_location STRING,
  display_lines STRING,
  session_date DATETIME
);

DROP TABLE IF EXISTS `capublic.bill_tbl`;
CREATE TABLE `capublic.bill_tbl` (
  bill_id STRING NOT NULL,
  session_year STRING NOT NULL,
  session_num STRING NOT NULL,
  measure_type STRING NOT NULL,
  measure_num INT64 NOT NULL,
  measure_state STRING NOT NULL,
  chapter_year STRING,
  chapter_type STRING,
  chapter_session_num STRING,
  chapter_num STRING,
  latest_bill_version_id STRING,
  active_flg STRING,
  trans_uid STRING,
  trans_update DATETIME,
  current_location STRING,
  current_secondary_loc STRING,
  current_house STRING,
  current_status STRING,
  days_31st_in_print DATETIME
);

DROP TABLE IF EXISTS `capublic.bill_version_authors_tbl`;
CREATE TABLE `capublic.bill_version_authors_tbl` (
  bill_version_id STRING NOT NULL,
  type STRING NOT NULL,
  house STRING,
  name STRING,
  contribution STRING,
  committee_members STRING,
  active_flg STRING,
  trans_uid STRING,
  trans_update DATETIME,
  primary_author_flg STRING
);

DROP TABLE IF EXISTS `capublic.bill_version_tbl`;
CREATE TABLE `capublic.bill_version_tbl` (
  bill_version_id STRING NOT NULL,
  bill_id STRING NOT NULL,
  version_num INT64 NOT NULL,
  bill_version_action_date DATETIME NOT NULL,
  bill_version_action STRING,
  request_num STRING,
  subject STRING,
  vote_required STRING,
  appropriation STRING,
  fiscal_committee STRING,
  local_program STRING,
  substantive_changes STRING,
  urgency STRING,
  taxlevy STRING,
  bill_xml STRING,
  active_flg STRING,
  trans_uid STRING,
  trans_update DATETIME
);

DROP TABLE IF EXISTS `capublic.codes_tbl`;
CREATE TABLE `capublic.codes_tbl` (
  code STRING,
  title STRING
);

DROP TABLE IF EXISTS `capublic.committee_hearing_tbl`;
CREATE TABLE `capublic.committee_hearing_tbl` (
  bill_id STRING,
  committee_type STRING,
  committee_nr INT64,
  hearing_date DATETIME,
  location_code STRING,
  trans_uid STRING,
  trans_update_date DATETIME
);

DROP TABLE IF EXISTS `capublic.daily_file_tbl`;
CREATE TABLE `capublic.daily_file_tbl` (
  bill_id STRING,
  location_code STRING,
  consent_calendar_code INT64,
  file_location STRING,
  publication_date DATETIME,
  floor_manager STRING,
  trans_uid STRING,
  trans_update_date DATETIME,
  session_num STRING,
  status STRING
);

DROP TABLE IF EXISTS `capublic.law_section_tbl`;
CREATE TABLE `capublic.law_section_tbl` (
  id STRING,
  law_code STRING,
  section_num STRING,
  op_statues STRING,
  op_chapter STRING,
  op_section STRING,
  effective_date DATETIME,
  law_section_version_id STRING,
  division STRING,
  title STRING,
  part STRING,
  chapter STRING,
  article STRING,
  history STRING,
  content_xml STRING,
  active_flg STRING,
  trans_uid STRING,
  trans_update DATETIME
);

DROP TABLE IF EXISTS `capublic.law_toc_sections_tbl`;
CREATE TABLE `capublic.law_toc_sections_tbl` (
  id STRING,
  law_code STRING,
  node_treepath STRING,
  section_num STRING,
  section_order NUMERIC,
  title STRING,
  op_statues STRING,
  op_chapter STRING,
  op_section STRING,
  trans_uid STRING,
  trans_update DATETIME,
  law_section_version_id STRING,
  seq_num NUMERIC
);

DROP TABLE IF EXISTS `capublic.law_toc_tbl`;
CREATE TABLE `capublic.law_toc_tbl` (
  law_code STRING,
  division STRING,
  title STRING,
  part STRING,
  chapter STRING,
  article STRING,
  heading STRING,
  active_flg STRING,
  trans_uid STRING,
  trans_update DATETIME,
  node_sequence NUMERIC,
  node_level NUMERIC,
  node_position NUMERIC,
  node_treepath STRING,
  contains_law_sections STRING,
  history_note STRING,
  op_statues STRING,
  op_chapter STRING,
  op_section STRING
);

DROP TABLE IF EXISTS `capublic.legislator_tbl`;
CREATE TABLE `capublic.legislator_tbl` (
  district STRING NOT NULL,
  session_year STRING,
  legislator_name STRING,
  house_type STRING,
  author_name STRING,
  first_name STRING,
  last_name STRING,
  middle_initial STRING,
  name_suffix STRING,
  name_title STRING,
  web_name_title STRING,
  party STRING,
  active_flg STRING NOT NULL,
  trans_uid STRING,
  trans_update DATETIME,
  active_legislator STRING
);

DROP TABLE IF EXISTS `capublic.location_code_tbl`;
CREATE TABLE `capublic.location_code_tbl` (
  session_year STRING,
  location_code STRING NOT NULL,
  location_type STRING NOT NULL,
  consent_calendar_code STRING,
  description STRING,
  long_description STRING,
  active_flg STRING,
  trans_uid STRING,
  trans_update DATETIME,
  inactive_file_flg STRING
);

DROP TABLE IF EXISTS `capublic.veto_message_tbl`;
CREATE TABLE `capublic.veto_message_tbl` (
  bill_id STRING,
  veto_date DATETIME,
  message STRING,
  trans_uid STRING,
  trans_update DATETIME
);

DROP TABLE IF EXISTS `capublic.committee_agenda_tbl`;
CREATE TABLE `capublic.committee_agenda_tbl` (
  committee_code STRING,
  committee_desc STRING,
  agenda_date DATETIME,
  agenda_time STRING,
  line1 STRING,
  line2 STRING,
  line3 STRING,
  building_type STRING,
  room_num STRING
);

-- --------------------------  E N D   O F  C O D E  ----------------