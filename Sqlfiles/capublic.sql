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

SET FOREIGN_KEY_CHECKS = 0;

-- -------------------------------------
-- Database
-- -------------------------------------
CREATE DATABASE IF NOT EXISTS `capublic`
  CHARACTER SET utf8 COLLATE  utf8_general_ci;
USE `capublic`;

GRANT ALL ON capublic.* TO capublic@'%' IDENTIFIED BY 'capublic';

-- -------------------------------------
-- Tables
-- -------------------------------------
DROP TABLE IF EXISTS `capublic`.`bill_analysis_tbl`;
CREATE TABLE `capublic`.`bill_analysis_tbl`     (
  `analysis_id`                 DECIMAL(22, 0)          NOT NULL,
  `bill_id`                     VARCHAR(20)       NOT NULL,
  `house`                       VARCHAR(1)        NULL,
  `analysis_type`               VARCHAR(100)      NULL,
  `committee_code`              VARCHAR(6)        NULL,
  `committee_name`              VARCHAR(200)      NULL,
  `amendment_author`            VARCHAR(100)      NULL,
  `analysis_date`               DATETIME                NULL,
  `amendment_date`              DATETIME                NULL,
  `page_num`                    DECIMAL(22, 0)          NULL,
  `source_doc`                  LONGBLOB                NULL,
  `released_floor`              VARCHAR(1)        NULL,
  `active_flg`                  VARCHAR(1)        NULL DEFAULT 'Y',
  `trans_uid`                   VARCHAR(20)       NULL,
  `trans_update`                DATETIME                NULL,
  PRIMARY KEY (`analysis_id`),
  INDEX `bill_analysis_bill_id_idx`  (`bill_id`(20))
)
ENGINE = INNODB
CHARACTER SET utf8 COLLATE utf8_general_ci;

DROP TABLE IF EXISTS `capublic`.`bill_detail_vote_tbl`;
CREATE TABLE `capublic`.`bill_detail_vote_tbl`  (
  `bill_id`                     VARCHAR(20)       NOT NULL,
  `location_code`               VARCHAR(6)        NOT NULL,
  `legislator_name`             VARCHAR(50)       NOT NULL,
  `vote_date_time`              DATETIME                NOT NULL,
  `vote_date_seq`               INT(4)                  NOT NULL,
  `vote_code`                   VARCHAR(5)        NULL,
  `motion_id`                   INT(8)                  NOT NULL,
  `trans_uid`                   VARCHAR(30)       NULL,
  `trans_update`                DATETIME                NULL,
  `member_order`                INT(4)                  NULL,
  `session_date`                DATETIME                NULL,
  `speaker`                     VARCHAR(1)        NULL,
  INDEX `author_votecode_idx`   (`legislator_name`(50), `vote_code`(5)),
  INDEX `bill_detail_vote_id_idx`       (`bill_id`(20)),
  INDEX `check_dup_detail_vote_idx`     (`bill_id`(20), `vote_date_time`, `location_code`(6), `motion_id`, `legislator_name`(50), `vote_date_seq`)
)
ENGINE = INNODB
CHARACTER SET utf8 COLLATE utf8_general_ci;

DROP TABLE IF EXISTS `capublic`.`bill_history_tbl`;
CREATE TABLE `capublic`.`bill_history_tbl`      (
  `bill_id`                     VARCHAR(20)       NULL,
  `bill_history_id`             DECIMAL(20, 0)          NULL,
  `action_date`                 DATETIME                NULL,
  `action`                      VARCHAR(2000)     NULL,
  `trans_uid`                   VARCHAR(20)       NULL,
  `trans_update_dt`             DATETIME                NULL,
  `action_sequence`             INT(4)                  NULL,
  `action_code`                 VARCHAR(5)        NULL,
  `action_status`               VARCHAR(60)       NULL,
  `primary_location`            VARCHAR(60)       NULL,
  `secondary_location`          VARCHAR(60)       NULL,
  `ternary_location`            VARCHAR(60)       NULL,
  `end_status`                  VARCHAR(60)       NULL,
  INDEX `bill_history_id_idx`   (`bill_id`(20))
)
ENGINE = INNODB
CHARACTER SET utf8 COLLATE utf8_general_ci;

DROP TABLE IF EXISTS `capublic`.`bill_motion_tbl`;
CREATE TABLE `capublic`.`bill_motion_tbl`       (
  `motion_id`                   DECIMAL(20, 0)          NOT NULL,
  `motion_text`                 VARCHAR(250)      NULL,
  `trans_uid`                   VARCHAR(30)       NULL,
  `trans_update`                DATETIME                NULL,
  PRIMARY KEY (`motion_id`)
)
ENGINE = INNODB
CHARACTER SET utf8 COLLATE utf8_general_ci;

DROP TABLE IF EXISTS `capublic`.`bill_summary_vote_tbl`;
CREATE TABLE `capublic`.`bill_summary_vote_tbl` (
  `bill_id`                     VARCHAR(20)       NOT NULL,
  `location_code`               VARCHAR(6)        NOT NULL,
  `vote_date_time`              DATETIME                NOT NULL,
  `vote_date_seq`               INT(4)                  NOT NULL,
  `motion_id`                   INT(8)                  NOT NULL,
  `ayes`                        INT(3)                  NULL,
  `noes`                        INT(3)                  NULL,
  `abstain`                     INT(3)                  NULL,
  `vote_result`                 VARCHAR(6)        NULL,
  `trans_uid`                   VARCHAR(30)       NULL,
  `trans_update`                DATETIME                NULL,
  `file_item_num`               VARCHAR(10)       NULL,
  `file_location`               VARCHAR(50)       NULL,
  `display_lines`               VARCHAR(2000)     NULL,
  `session_date`                DATETIME                NULL,
  INDEX `bill_summary_vote_id_idx`      (`bill_id`(20)),
  INDEX `bill_summary_vote_mo_idx`      (`motion_id`),
  INDEX `check_dup_summary_vote_idx`    (`bill_id`(20), `motion_id`, `vote_date_time`, `vote_date_seq`, `location_code`(6))
)
ENGINE = INNODB
CHARACTER SET utf8 COLLATE utf8_general_ci;

DROP TABLE IF EXISTS `capublic`.`bill_tbl`;
CREATE TABLE `capublic`.`bill_tbl`      (
  `bill_id`                     VARCHAR(19)       NOT NULL,
  `session_year`                VARCHAR(8)        NOT NULL,
  `session_num`                 VARCHAR(2)        NOT NULL,
  `measure_type`                VARCHAR(4)        NOT NULL,
  `measure_num`                 INT(5)                  NOT NULL,
  `measure_state`               VARCHAR(40)       NOT NULL,
  `chapter_year`                VARCHAR(4)        NULL,
  `chapter_type`                VARCHAR(10)       NULL,
  `chapter_session_num`         VARCHAR(2)        NULL,
  `chapter_num`                 VARCHAR(10)       NULL,
  `latest_bill_version_id`      VARCHAR(30)       NULL,
  `active_flg`                  VARCHAR(1)        NULL DEFAULT 'Y',
  `trans_uid`                   VARCHAR(30)       NULL,
  `trans_update`                DATETIME                NULL,
  `current_location`            VARCHAR(200)      NULL,
  `current_secondary_loc`       VARCHAR(60)       NULL,
  `current_house`               VARCHAR(60)       NULL,
  `current_status`              VARCHAR(60)       NULL,
  `days_31st_in_print`          DATETIME                NULL,
  PRIMARY KEY (`bill_id`),
  INDEX `bill_tbl_chapter_year_idx`     (`chapter_year`(4)),
  INDEX `bill_tbl_measure_num_idx`      (`measure_num`),
  INDEX `bill_tbl_measure_type_idx`     (`measure_type`(4)),
  INDEX `bill_tbl_session_idx`          (`session_year`(8)),
  INDEX `bill_tbl__ltst_bill_ver_idx`   (`latest_bill_version_id`(30))
)
ENGINE = INNODB
CHARACTER SET utf8 COLLATE utf8_general_ci;

DROP TABLE IF EXISTS `capublic`.`bill_version_authors_tbl`;
CREATE TABLE `capublic`.`bill_version_authors_tbl`      (
  `bill_version_id`             VARCHAR(30)       NOT NULL,
  `type`                        VARCHAR(15)       NOT NULL,
  `house`                       VARCHAR(100)      NULL,
  `name`                        VARCHAR(100)      NULL,
  `contribution`                VARCHAR(100)      NULL,
  `committee_members`           VARCHAR(2000)     NULL,
  `active_flg`                  VARCHAR(1)        NULL DEFAULT 'Y',
  `trans_uid`                   VARCHAR(30)       NULL,
  `trans_update`                DATETIME                NULL,
  `primary_author_flg`          VARCHAR(1)        NULL DEFAULT 'N',
  INDEX `bill_version_auth_tbl_id_idx`  (`bill_version_id`(30)),
  Index `bill_version_auth_tbl_name_idx` (`name`)
)
ENGINE = INNODB
CHARACTER SET utf8 COLLATE utf8_general_ci;

DROP TABLE IF EXISTS `capublic`.`bill_version_tbl`;
CREATE TABLE `capublic`.`bill_version_tbl`      (
  `bill_version_id`             VARCHAR(30)       NOT NULL,
  `bill_id`                     VARCHAR(19)       NOT NULL,
  `version_num`                 INT(2)                  NOT NULL,
  `bill_version_action_date`    DATETIME                NOT NULL,
  `bill_version_action`         VARCHAR(100)      NULL,
  `request_num`                 VARCHAR(10)       NULL,
  `subject`                     VARCHAR(1000)     NULL,
  `vote_required`               VARCHAR(100)      NULL,
  `appropriation`               VARCHAR(3)        NULL,
  `fiscal_committee`            VARCHAR(3)        NULL,
  `local_program`               VARCHAR(3)        NULL,
  `substantive_changes`         VARCHAR(3)        NULL,
  `urgency`                     VARCHAR(3)        NULL,
  `taxlevy`                     VARCHAR(3)        NULL,
  `bill_xml`                    LONGTEXT          NULL,
  `active_flg`                  VARCHAR(1)        NULL DEFAULT 'Y',
  `trans_uid`                   VARCHAR(30)       NULL,
  `trans_update`                DATETIME                NULL,
  PRIMARY KEY (`bill_version_id`),
  Index `bill_version_tbl_bill_id_idx` (`bill_id`(19)),
  Index `bill_version_tbl_version_idx` (`version_num`)
)
ENGINE = INNODB
CHARACTER SET utf8 COLLATE utf8_general_ci;

DROP TABLE IF EXISTS `capublic`.`codes_tbl`;
CREATE TABLE `capublic`.`codes_tbl`     (
  `code`                        VARCHAR(5)        NULL,
  `title`                       VARCHAR(2000)     NULL
)
ENGINE = INNODB
CHARACTER SET utf8 COLLATE utf8_general_ci;

DROP TABLE IF EXISTS `capublic`.`committee_hearing_tbl`;
CREATE TABLE `capublic`.`committee_hearing_tbl` (
  `bill_id`                     VARCHAR(20)       NULL,
  `committee_type`              VARCHAR(2)        NULL,
  `committee_nr`                INT(5)                  NULL,
  `hearing_date`                DATETIME                NULL,
  `location_code`               VARCHAR(6)        NULL,
  `trans_uid`                   VARCHAR(30)       NULL,
  `trans_update_date`           DATETIME                NULL,
  Index `committee_hear_bill_id_idx` (`bill_id`(20))
)
ENGINE = INNODB
CHARACTER SET utf8 COLLATE utf8_general_ci;

DROP TABLE IF EXISTS `capublic`.`daily_file_tbl`;
CREATE TABLE `capublic`.`daily_file_tbl`        (
  `bill_id`                     VARCHAR(20)       NULL,
  `location_code`               VARCHAR(6)        NULL,
  `consent_calendar_code`       INT(2)                  NULL,
  `file_location`               VARCHAR(6)        NULL,
  `publication_date`            DATETIME                NULL,
  `floor_manager`               VARCHAR(100)      NULL,
  `trans_uid`                   VARCHAR(20)       NULL,
  `trans_update_date`           DATETIME                NULL,
  `session_num`                 VARCHAR(2)        NULL,
  `status`                      VARCHAR(200)      NULL,
  Index `daily_file_pub_date_idx` (`publication_date`),
  Index `daily_file_tbl_bill_id_idx` (`bill_id`(20))
)
ENGINE = INNODB
CHARACTER SET utf8 COLLATE utf8_general_ci;

DROP TABLE IF EXISTS `capublic`.`law_section_tbl`;
CREATE TABLE `capublic`.`law_section_tbl`       (
  `id`                          VARCHAR(100)      NULL,
  `law_code`                    VARCHAR(5)        NULL,
  `section_num`                 VARCHAR(30)       NULL,
  `op_statues`                  VARCHAR(10)       NULL,
  `op_chapter`                  VARCHAR(10)       NULL,
  `op_section`                  VARCHAR(20)       NULL,
  `effective_date`              DATETIME                NULL,
  `law_section_version_id`      VARCHAR(100)      NULL,
  `division`                    VARCHAR(100)      NULL,
  `title`                       VARCHAR(100)      NULL,
  `part`                        VARCHAR(100)      NULL,
  `chapter`                     VARCHAR(100)      NULL,
  `article`                     VARCHAR(100)      NULL,
  `history`                     VARCHAR(1000)     NULL,
  `content_xml`                 LONGTEXT          NULL,
  `active_flg`                  VARCHAR(1)        NULL DEFAULT 'Y',
  `trans_uid`                   VARCHAR(30)       NULL,
  `trans_update`                DATETIME                NULL,
  INDEX `law_section_tbl_pk`   (`id`(100)),
  Index `law_section_code_idx` (`law_code`(5)),
  Index `law_section_id_idx` (`law_section_version_id`(100)),
  Index `law_section_sect_idx` (`section_num`(30))
)
ENGINE = INNODB
CHARACTER SET utf8 COLLATE utf8_general_ci;

DROP TABLE IF EXISTS `capublic`.`law_toc_sections_tbl`;
CREATE TABLE `capublic`.`law_toc_sections_tbl`  (
  `id`                          VARCHAR(100)      NULL,
  `law_code`                    VARCHAR(5)        NULL,
  `node_treepath`               VARCHAR(100)      NULL,
  `section_num`                 VARCHAR(30)       NULL,
  `section_order`               DECIMAL(22, 0)          NULL,
  `title`                       VARCHAR(400)      NULL,
  `op_statues`                  VARCHAR(10)       NULL,
  `op_chapter`                  VARCHAR(10)       NULL,
  `op_section`                  VARCHAR(20)       NULL,
  `trans_uid`                   VARCHAR(30)       NULL,
  `trans_update`                DATETIME                NULL,
  `law_section_version_id`      VARCHAR(100)      NULL,
  `seq_num`                     DECIMAL(22, 0)          NULL,
  Index `law_toc_sections_node_idx` (`law_code`(5), `node_treepath`(100))
)
ENGINE = INNODB
CHARACTER SET utf8 COLLATE utf8_general_ci;

DROP TABLE IF EXISTS `capublic`.`law_toc_tbl`;
CREATE TABLE `capublic`.`law_toc_tbl`   (
  `law_code`                    VARCHAR(5)        NULL,
  `division`                    VARCHAR(100)      NULL,
  `title`                       VARCHAR(100)      NULL,
  `part`                        VARCHAR(100)      NULL,
  `chapter`                     VARCHAR(100)      NULL,
  `article`                     VARCHAR(100)      NULL,
  `heading`                     VARCHAR(2000)     NULL,
  `active_flg`                  VARCHAR(1)        NULL DEFAULT 'Y',
  `trans_uid`                   VARCHAR(30)       NULL,
  `trans_update`                DATETIME                NULL,
  `node_sequence`               DECIMAL(22, 0)          NULL,
  `node_level`                  DECIMAL(22, 0)          NULL,
  `node_position`               DECIMAL(22, 0)          NULL,
  `node_treepath`               VARCHAR(100)      NULL,
  `contains_law_sections`       VARCHAR(1)        NULL,
  `history_note`                VARCHAR(350)      NULL,
  `op_statues`                  VARCHAR(10)       NULL,
  `op_chapter`                  VARCHAR(10)       NULL,
  `op_section`                  VARCHAR(20)       NULL,
  Index `law_toc_article_idx` (`article`(100)),
  Index `law_toc_chapter_idx` (`chapter`(100)),
  Index `law_toc_code_idx` (`law_code`(5)),
  Index `law_toc_division_idx` (`division`(100)),
  Index `law_toc_part_idx` (`part`(100)),
  Index `law_toc_title_idx` (`title`(100))
)
ENGINE = INNODB
CHARACTER SET utf8 COLLATE utf8_general_ci;

DROP TABLE IF EXISTS `capublic`.`legislator_tbl`;
CREATE TABLE `capublic`.`legislator_tbl`        (
  `district`                    VARCHAR(5)        NOT NULL,
  `session_year`                VARCHAR(8)        NULL,
  `legislator_name`             VARCHAR(30)       NULL,
  `house_type`                  VARCHAR(1)        NULL,
  `author_name`                 VARCHAR(200)      NULL,
  `first_name`                  VARCHAR(30)       NULL,
  `last_name`                   VARCHAR(30)       NULL,
  `middle_initial`              VARCHAR(1)        NULL,
  `name_suffix`                 VARCHAR(12)       NULL,
  `name_title`                  VARCHAR(34)       NULL,
  `web_name_title`              VARCHAR(34)       NULL,
  `party`                       VARCHAR(4)        NULL,
  `active_flg`                  VARCHAR(1)        NOT NULL DEFAULT 'Y',
  `trans_uid`                   VARCHAR(30)       NULL,
  `trans_update`                DATETIME                NULL,
  `active_legislator`           VARCHAR(1)        NULL DEFAULT 'Y'
)
ENGINE = INNODB
CHARACTER SET utf8 COLLATE utf8_general_ci;

DROP TABLE IF EXISTS `capublic`.`location_code_tbl`;
CREATE TABLE `capublic`.`location_code_tbl`     (
  `session_year`                VARCHAR(8)        NULL,
  `location_code`               VARCHAR(6)        NOT NULL,
  `location_type`               VARCHAR(1)        NOT NULL,
  `consent_calendar_code`       VARCHAR(2)        NULL,
  `description`                 VARCHAR(60)       NULL,
  `long_description`            VARCHAR(200)      NULL,
  `active_flg`                  VARCHAR(1)        NULL DEFAULT 'Y',
  `trans_uid`                   VARCHAR(30)       NULL,
  `trans_update`                DATETIME                NULL,
  `inactive_file_flg`           VARCHAR(1)        NULL,
  INDEX `location_code_tbl_pk1`       (`location_code`(6)),
  Index `localtion_code_session_idx1` (`session_year`(8))
)
ENGINE = INNODB
CHARACTER SET utf8 COLLATE utf8_general_ci;

DROP TABLE IF EXISTS `capublic`.`veto_message_tbl`;
CREATE TABLE `capublic`.`veto_message_tbl` (
  `bill_id`                     varchar(20)       NULL,
  `veto_date`                   datetime                NULL,
  `message`                     longtext          NULL,
  `trans_uid`                   varchar(20)       NULL,
  `trans_update`                datetime                NULL
)
ENGINE = INNODB
CHARACTER SET utf8 COLLATE utf8_general_ci;

DROP TABLE IF EXISTS `capublic`.`committee_agenda_tbl`;
CREATE TABLE `capublic`.`committee_agenda_tbl` (
  `committee_code`       varchar(200)      NULL,
  `committee_desc`       varchar(1000)     NULL,
  `agenda_date`          datetime                NULL,
  `agenda_time`          varchar(200)      NULL,
  `line1`                varchar(500)      NULL,
  `line2`                varchar(500)      NULL,
  `line3`                varchar(500)      NULL,
  `building_type`        varchar(200)      NULL,
  `room_num`             varchar(100)      NULL
)
ENGINE = INNODB
CHARACTER SET utf8 COLLATE utf8_general_ci;


SET FOREIGN_KEY_CHECKS = 1;

-- --------------------------  E N D   O F  C O D E  --------------------------+
