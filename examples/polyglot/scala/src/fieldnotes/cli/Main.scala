package fieldnotes.cli

import fieldnotes.domain.Transition

object Main {
  def main(args: Array[String]): Unit = {
    scala.io.Source.stdin.getLines().foreach { line =>
      line.split("\t", -1).toList match {
        case id :: role :: session :: issue :: current :: requested :: Nil =>
          println(s"$id\t${Transition.decide(role, session, issue, current, requested)}")
        case _ => throw new IllegalArgumentException("Expected six TSV fields")
      }
    }
  }
}
