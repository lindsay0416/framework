from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable
import configparser
import os


class neoUtility:

    #构造方法
    def __init__(self):
        #读取配置文件
        pro_dir = os.path.split(os.path.realpath(__file__))[0]
        config_path = os.path.join(pro_dir, "config.ini")
        #if not os.path.exists(config_path):print("无配置文件")
        config = configparser.ConfigParser()
        config.read(config_path)
        #配置neo4j数据库连接参数
        # uri = "neo4j:http://localhost:7474"
        # user = "neo4j"
        # password = "admin"
        uri = config.get("config","uri")
        user = config.get("config","user")
        password = config.get("config","password")
        #创建neo4j驱动对象
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    #关闭neo4j数据库连接
    def close(self):
        self.driver.close()

    #在数据库中创建Entity
    #entity_cate： 创建Entity的类型
    #entity_name： 创建Entity的名称
    def create_entity(self, entity_cate, entity_name):
        with self.driver.session() as session:
            result = session.write_transaction(self._create_and_return_entity, entity_cate, entity_name)
            for record in result:
                print("Created entity: {name: " + record["e"] + "}")

    @staticmethod
    def _create_and_return_entity(tx, entity_cate, entity_name):
        query = (
            "CREATE (e:"+entity_cate+"{ name: $entity_name }) "
            "RETURN e"
        )
        result = tx.run(query, entity_name=entity_name)
        try:
            return [{"e": record["e"]["name"]}for record in result]

        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def create_relation():

    

    

    def find_entity(self, entity_cate, entity_name):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_entity, entity_cate, entity_name)
            for record in result:
                print("Found entity: {record}".format(record=record))

    @staticmethod
    def _find_and_return_entity(tx, entity_cate, entity_name):
        query = (
            "MATCH (e:" + entity_cate + ")"
            "WHERE e.name = $entity_name"
            "RETURN e.name AS name"
        )
        result = tx.run(query, entity_name=entity_name)
        return [record["name"] for record in result]