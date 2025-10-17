#!/usr/bin/env python3
"""
CLI命令基类

定义所有CLI命令的通用接口和行为。
"""

from abc import ABC, abstractmethod
from typing import Any
import argparse


class BaseCommand(ABC):
    """CLI命令基类"""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def create_parser(self, subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
        """创建命令的参数解析器"""
        pass

    @abstractmethod
    def execute(self, args: argparse.Namespace) -> int:
        """执行命令"""
        pass

    def print_error(self, message: str) -> None:
        """打印错误信息"""
        print(f"❌ {message}")

    def print_success(self, message: str) -> None:
        """打印成功信息"""
        print(f"✅ {message}")

    def print_info(self, message: str) -> None:
        """打印信息"""
        print(f"ℹ️  {message}")

    def print_warning(self, message: str) -> None:
        """打印警告信息"""
        print(f"⚠️  {message}")